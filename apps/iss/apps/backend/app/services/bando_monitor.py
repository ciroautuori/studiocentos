"""
Servizio integrato di monitoraggio bandi per ISS
Adattato dal sistema bot originale per l'integrazione nel backend FastAPI
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib
import re
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bando import Bando, BandoSource, BandoStatus
from app.models.bando_config import BandoConfig, BandoLog
from app.crud.bando import bando_crud
from app.core.config import settings

logger = logging.getLogger(__name__)


class BandoMonitorService:
    """Servizio per il monitoraggio automatico dei bandi"""
    
    def __init__(self):
        self.session = None
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            headers={'User-Agent': self.user_agent},
            timeout=30.0
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    def generate_hash(self, title: str, ente: str, link: str) -> str:
        """Genera hash univoco per identificare un bando"""
        content = f"{title}_{ente}_{link}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def parse_date(self, date_string: str) -> Optional[datetime]:
        """Converte una stringa di data in oggetto datetime"""
        if not date_string:
            return None
        
        # Pattern comuni per le date italiane
        patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # dd/mm/yyyy o dd-mm-yyyy
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # yyyy/mm/dd o yyyy-mm-dd
            r'(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+(\d{4})'
        ]
        
        mesi = {
            'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4,
            'maggio': 5, 'giugno': 6, 'luglio': 7, 'agosto': 8,
            'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12
        }
        
        for pattern in patterns:
            match = re.search(pattern, date_string.lower())
            if match:
                try:
                    if 'gennaio' in pattern:  # Formato testuale
                        day, month_name, year = match.groups()
                        month = mesi[month_name]
                        return datetime(int(year), month, int(day))
                    elif pattern.startswith(r'(\d{4})'):  # yyyy-mm-dd
                        year, month, day = match.groups()
                        return datetime(int(year), int(month), int(day))
                    else:  # dd/mm/yyyy
                        day, month, year = match.groups()
                        return datetime(int(year), int(month), int(day))
                except (ValueError, KeyError):
                    continue
        
        return None
    
    def is_valid_deadline(self, deadline_str: str, min_days: int = 30) -> bool:
        """Verifica se la scadenza è valida"""
        deadline = self.parse_date(deadline_str)
        if not deadline:
            return False
        
        cutoff_date = datetime.now() + timedelta(days=min_days)
        return deadline > cutoff_date
    
    def contains_keywords(self, text: str, keywords: List[str]) -> Optional[str]:
        """Verifica se il testo contiene parole chiave rilevanti"""
        if not text or not keywords:
            return None
        
        text_lower = text.lower()
        matched_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched_keywords.append(keyword)
        
        return ", ".join(matched_keywords) if matched_keywords else None
    
    async def scrape_comune_salerno(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Comune di Salerno"""
        bandi = []
        try:
            url = "https://www.comune.salerno.it/amministrazioneTrasparente/bandi-di-concorso"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Adatta il selettore al sito reale
            for item in soup.find_all('div', class_='bando-item', limit=20):
                try:
                    title_elem = item.find('h3') or item.find('h2') or item.find('a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link_elem = item.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else ""
                    
                    # Cerca scadenza
                    deadline_elem = item.find(string=re.compile(r'scadenza|entro', re.I))
                    deadline = deadline_elem.strip() if deadline_elem else ""
                    
                    # Descrizione
                    desc_elem = item.find('p') or item.find('div', class_='descrizione')
                    descrizione = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Verifica keywords
                    full_text = f"{title} {descrizione}".lower()
                    keyword_match = self.contains_keywords(full_text, keywords)
                    
                    if keyword_match and self.is_valid_deadline(deadline, config.min_deadline_days):
                        bandi.append({
                            'title': title[:500],
                            'ente': 'Comune di Salerno',
                            'scadenza_raw': deadline[:100],
                            'link': link,
                            'descrizione': descrizione[:1000],
                            'fonte': BandoSource.COMUNE_SALERNO,
                            'keyword_match': keyword_match
                        })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing singolo bando Comune Salerno: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Comune Salerno: {e}")
            
        return bandi
    
    async def scrape_regione_campania(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Regione Campania"""
        bandi = []
        try:
            url = "https://fse.regione.campania.it/bando-pubblico-per-sostegno-a-iniziative-e-progetti-locali-in-favore-di-organizzazioni-di-volontariato-associazioni-di-promozione-sociale-e-fondazioni-ets-onlus-scheda-avviso/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for item in soup.find_all('div', class_='bando-regione', limit=15):
                try:
                    title_elem = item.find('h3') or item.find('a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link_elem = item.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else ""
                    
                    # Cerca informazioni
                    info_text = item.get_text()
                    deadline_match = re.search(r'scadenza[:\s]*([0-9/\-\s\w]+)', info_text, re.I)
                    deadline = deadline_match.group(1) if deadline_match else ""
                    
                    keyword_match = self.contains_keywords(info_text, keywords)
                    
                    if keyword_match and self.is_valid_deadline(deadline, config.min_deadline_days):
                        bandi.append({
                            'title': title[:500],
                            'ente': 'Regione Campania',
                            'scadenza_raw': deadline[:100],
                            'link': link,
                            'descrizione': info_text[:1000],
                            'fonte': BandoSource.REGIONE_CAMPANIA,
                            'keyword_match': keyword_match
                        })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing bando Regione Campania: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Regione Campania: {e}")
            
        return bandi
    
    async def scrape_granter_campania(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Granter.it - Bandi Campania REALI"""
        bandi = []
        try:
            url = "https://granter.it/cerca-bandi/campania/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca tutti i link ai bandi
            for link_elem in soup.find_all('a', href=True, limit=20):
                try:
                    href = link_elem.get('href', '')
                    
                    # Solo link a bandi/opportunità
                    if not ('/bandi/' in href or '/opportunita/' in href):
                        continue
                    
                    # Estrai titolo
                    title = link_elem.get_text(strip=True)
                    if not title or len(title) < 10:
                        continue
                    
                    # Cerca ente promotore nel parent
                    parent = link_elem.find_parent(['div', 'article', 'section'])
                    ente = "Vari enti"
                    if parent:
                        ente_text = parent.get_text()
                        if 'Fondazione Con il Sud' in ente_text:
                            ente = 'Fondazione Con il Sud'
                        elif 'Fondazione' in ente_text:
                            ente = 'Fondazione Charlemagne'
                        elif 'Regione' in ente_text:
                            ente = 'Regione Campania'
                    
                    # Cerca scadenza
                    scadenza_raw = ""
                    if parent:
                        scadenza_match = re.search(r'Scadenza[:\s]*(\d{1,2}\s+\w+\s+\d{4})', parent.get_text())
                        if scadenza_match:
                            scadenza_raw = scadenza_match.group(1)
                        elif 'Nessuna scadenza' in parent.get_text():
                            scadenza_raw = 'Sempre attivo'
                    
                    # Full URL
                    full_link = urljoin(url, href)
                    
                    # Keyword matching
                    full_text = f"{title} {ente}"
                    keyword_match = self.contains_keywords(full_text, keywords)
                    
                    # PRENDI TUTTI i bandi senza filtro (per ora)
                    bandi.append({
                        'title': title[:500],
                        'ente': ente,
                        'scadenza_raw': scadenza_raw[:100],
                        'link': full_link,
                        'descrizione': f"Bando/opportunità per {ente} in Campania",
                        'fonte': BandoSource.FONDAZIONE_COMUNITA,
                        'keyword_match': keyword_match or "campania, terzo settore"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing singolo bando Granter: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Granter: {e}")
            
        return bandi
    
    async def scrape_fondazione_comunita_salernitana(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Fondazione Comunità Salernitana - SITO SPECIFICO"""
        bandi = []
        try:
            url = "https://innovazionesociale.org/index.php/14-bandi-e-finanziamenti/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca articoli sui bandi
            for elem in soup.find_all(['article', 'div', 'li'], limit=10):
                try:
                    text = elem.get_text()
                    # Solo contenuti con parole chiave rilevanti
                    if not any(term in text.lower() for term in ['bando', 'fondazione', 'salernitana', 'aps', 'progetti']):
                        continue
                    
                    title_elem = elem.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 20:
                        continue
                    
                    # Cerca link
                    link_elem = elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    # Cerca importo
                    importo_match = re.search(r'(\d+\.?\d*\.?\d*)\s*euro', text, re.I)
                    importo = importo_match.group(1) + " euro" if importo_match else "Vedi bando"
                    
                    # Cerca scadenza
                    scadenza_raw = ""
                    scad_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text)
                    if scad_match:
                        scadenza_raw = scad_match.group(1)
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'Fondazione Comunità Salernitana',
                        'scadenza_raw': scadenza_raw,
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.FONDAZIONE_COMUNITA,
                        'importo': importo,
                        'categoria': 'sociale',
                        'keyword_match': keyword_match or "fondazione salernitana, locale"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing Fondazione Salernitana: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Fondazione Salernitana: {e}")
            
        return bandi
    
    async def scrape_regione_campania_bandi(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Regione Campania - Sezione Bandi di Concorso"""
        bandi = []
        try:
            url = "https://www.regione.campania.it/regione/it/amministrazione-trasparente-fy2n/bandi-di-concorso/bandi-di-concorso"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca bandi ufficiali
            for elem in soup.find_all(['tr', 'div', 'article'], limit=15):
                try:
                    text = elem.get_text()
                    # Solo bandi per terzo settore/APS
                    if not any(term in text.lower() for term in ['bando', 'aps', 'terzo settore', 'sociale', 'volontariato', 'associazioni']):
                        continue
                    
                    title_elem = elem.find(['td', 'h1', 'h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 15:
                        continue
                    
                    link_elem = elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    # Cerca scadenza
                    scadenza_raw = ""
                    scad_match = re.search(r'scadenza[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text, re.I)
                    if scad_match:
                        scadenza_raw = scad_match.group(1)
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'Regione Campania',
                        'scadenza_raw': scadenza_raw,
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.REGIONE_CAMPANIA,
                        'keyword_match': keyword_match or "regione campania, ufficiale"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing Regione Campania bandi: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Regione Campania bandi: {e}")
            
        return bandi
    
    async def scrape_comune_salerno_real(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Comune di Salerno - Amministrazione Trasparente"""
        bandi = []
        try:
            url = "http://www.comune.salerno.it/amministrazioneTrasparente/bandi-di-concorso"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca bandi comunali
            for elem in soup.find_all(['tr', 'div', 'li'], limit=15):
                try:
                    text = elem.get_text()
                    if not any(term in text.lower() for term in ['bando', 'avviso', 'concorso', 'sociale', 'cultura']):
                        continue
                    
                    title_elem = elem.find(['td', 'h1', 'h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    
                    link_elem = elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'Comune di Salerno',
                        'scadenza_raw': '',
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.COMUNE_SALERNO,
                        'keyword_match': keyword_match or "comune salerno, locale"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing Comune Salerno: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Comune Salerno: {e}")
            
        return bandi
    
    async def scrape_arci_servizio_civile(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping ARCI Servizio Civile Salerno/Campania"""
        bandi = []
        try:
            urls = [
                "https://www.arciserviziocivile.it/salerno",
                "https://www.arciserviziocivile.it/campania"
            ]
            
            for url in urls:
                try:
                    response = await self.session.get(url, timeout=config.timeout)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Cerca progetti di servizio civile
                    for elem in soup.find_all(['div', 'article', 'li'], limit=10):
                        try:
                            text = elem.get_text()
                            if not any(term in text.lower() for term in ['progetto', 'servizio civile', 'bando', 'volontari']):
                                continue
                            
                            title_elem = elem.find(['h1', 'h2', 'h3', 'h4'])
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            if len(title) < 15:
                                continue
                            
                            link_elem = elem.find('a', href=True)
                            link = urljoin(url, link_elem['href']) if link_elem else url
                            
                            keyword_match = self.contains_keywords(text, keywords)
                            
                            bandi.append({
                                'title': title[:500],
                                'ente': 'ARCI Servizio Civile',
                                'scadenza_raw': '',
                                'link': link,
                                'descrizione': text[:1000],
                                'fonte': BandoSource.CSV_SALERNO,
                                'categoria': 'servizio civile',
                                'keyword_match': keyword_match or "arci, servizio civile, volontari"
                            })
                                
                        except Exception as e:
                            logger.warning(f"Errore parsing ARCI: {e}")
                            continue
                            
                except Exception as e:
                    logger.warning(f"Errore ARCI URL {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping ARCI Servizio Civile: {e}")
            
        return bandi
    
    async def scrape_contributi_regione_campania(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Contributi Regione Campania - Portale aggregatore"""
        bandi = []
        try:
            url = "https://bandi.contributiregione.it/regione/campania"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca bandi regionali aggregati
            for elem in soup.find_all(['div', 'article', 'li'], class_=re.compile(r'bando|contributo'), limit=20):
                try:
                    title_elem = elem.find(['h1', 'h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 15:
                        continue
                    
                    text = elem.get_text()
                    
                    # Solo bandi per APS/terzo settore
                    if not any(term in text.lower() for term in ['aps', 'associazioni', 'sociale', 'terzo settore', 'volontariato']):
                        continue
                    
                    link_elem = elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    # Cerca scadenza
                    scadenza_raw = ""
                    scad_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text)
                    if scad_match:
                        scadenza_raw = scad_match.group(1)
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'Contributi Regione Campania',
                        'scadenza_raw': scadenza_raw,
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.REGIONE_CAMPANIA,
                        'keyword_match': keyword_match or "contributi regione, aggregatore"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing Contributi Regione: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Contributi Regione: {e}")
            
        return bandi
    
    async def scrape_regione_campania_news(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Regione Campania - Sezione News Ufficiale"""
        bandi = []
        try:
            url = "https://www.regione.campania.it/regione/it/news/regione-informa/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca articoli di news che contengono "bando" o "APS"
            for article in soup.find_all(['article', 'div', 'section'], limit=20):
                try:
                    text = article.get_text()
                    # Solo articoli con termini rilevanti
                    if not any(term in text.lower() for term in ['bando', 'aps', 'associazioni', 'terzo settore', 'volontariato']):
                        continue
                    
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 15:
                        continue
                    
                    # Cerca link
                    link_elem = article.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    # Cerca data/scadenza
                    scadenza_raw = ""
                    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text)
                    if date_match:
                        scadenza_raw = date_match.group(1)
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'Regione Campania',
                        'scadenza_raw': scadenza_raw,
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.REGIONE_CAMPANIA,
                        'keyword_match': keyword_match or "regione campania, ufficiale"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing Regione Campania: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Regione Campania: {e}")
            
        return bandi
    
    async def scrape_fse_regione_campania(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping FSE Regione Campania - Fondo Sociale Europeo"""
        bandi = []
        try:
            urls = [
                "https://fse.regione.campania.it/",
                "https://fse.regione.campania.it/bando-pubblico-per-sostegno-a-iniziative-e-progetti-locali-in-favore-di-organizzazioni-di-volontariato-associazioni-di-promozione-sociale-e-fondazioni-ets-onlus-scheda-avviso/"
            ]
            
            for url in urls:
                try:
                    response = await self.session.get(url, timeout=config.timeout)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Cerca contenuti relativi a bandi per APS
                    for elem in soup.find_all(['div', 'article', 'section'], limit=15):
                        try:
                            text = elem.get_text()
                            if not any(term in text.lower() for term in ['bando', 'aps', 'odv', 'ets', 'associazioni']):
                                continue
                            
                            title_elem = elem.find(['h1', 'h2', 'h3'])
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            if len(title) < 20:
                                continue
                            
                            link_elem = elem.find('a', href=True)
                            link = urljoin(url, link_elem['href']) if link_elem else url
                            
                            keyword_match = self.contains_keywords(text, keywords)
                            
                            bandi.append({
                                'title': title[:500],
                                'ente': 'FSE Regione Campania',
                                'scadenza_raw': '',
                                'link': link,
                                'descrizione': text[:1000],
                                'fonte': BandoSource.REGIONE_CAMPANIA,
                                'keyword_match': keyword_match or "fse, europeo, regione campania"
                            })
                                
                        except Exception as e:
                            logger.warning(f"Errore parsing FSE elemento: {e}")
                            continue
                            
                except Exception as e:
                    logger.warning(f"Errore FSE URL {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping FSE Campania: {e}")
            
        return bandi
    
    async def scrape_sviluppo_campania(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping Sviluppo Campania - Bandi Aperti"""
        bandi = []
        try:
            urls = [
                "https://www.sviluppocampania.it/bandi-aperti/",
                "https://bandi.sviluppocampania.it"
            ]
            
            for url in urls:
                try:
                    response = await self.session.get(url, timeout=config.timeout)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Cerca bandi attivi
                    for elem in soup.find_all(['div', 'article', 'li'], class_=re.compile(r'bando|post|entry'), limit=15):
                        try:
                            title_elem = elem.find(['h1', 'h2', 'h3', 'h4'])
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            if len(title) < 15:
                                continue
                            
                            text = elem.get_text()
                            
                            # Filtra solo bandi rilevanti per APS/terzo settore
                            if not any(term in text.lower() for term in ['aps', 'associazioni', 'terzo settore', 'sociale', 'volontariato']):
                                continue
                            
                            link_elem = elem.find('a', href=True)
                            link = urljoin(url, link_elem['href']) if link_elem else url
                            
                            # Cerca scadenza
                            scadenza_raw = ""
                            scad_match = re.search(r'scadenza[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text, re.I)
                            if scad_match:
                                scadenza_raw = scad_match.group(1)
                            
                            keyword_match = self.contains_keywords(text, keywords)
                            
                            bandi.append({
                                'title': title[:500],
                                'ente': 'Sviluppo Campania',
                                'scadenza_raw': scadenza_raw,
                                'link': link,
                                'descrizione': text[:1000],
                                'fonte': BandoSource.REGIONE_CAMPANIA,
                                'keyword_match': keyword_match or "sviluppo campania, bandi aperti"
                            })
                                
                        except Exception as e:
                            logger.warning(f"Errore parsing Sviluppo Campania: {e}")
                            continue
                            
                except Exception as e:
                    logger.warning(f"Errore Sviluppo Campania URL {url}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping Sviluppo Campania: {e}")
            
        return bandi
    
    async def scrape_csr_campania(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping CSR Campania - Piano Sviluppo Regionale"""
        bandi = []
        try:
            url = "https://psrcampaniacomunica.it/bandi-e-graduatorie/bandi/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca bandi CSR
            for elem in soup.find_all(['div', 'article', 'section'], limit=10):
                try:
                    text = elem.get_text()
                    if not any(term in text.lower() for term in ['bando', 'csr', 'campania', 'terzo settore']):
                        continue
                    
                    title_elem = elem.find(['h1', 'h2', 'h3'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 15:
                        continue
                    
                    link_elem = elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'CSR Campania',
                        'scadenza_raw': '',
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.REGIONE_CAMPANIA,
                        'keyword_match': keyword_match or "csr campania, piano sviluppo"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing CSR Campania: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping CSR Campania: {e}")
            
        return bandi
    
    async def scrape_csv_napoli(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping CSV Napoli - Bandi reali per APS"""
        bandi = []
        try:
            url = "https://www.csvnapoli.it/category/progettazione/bandi/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca articoli di bandi
            for article in soup.find_all(['article', 'div'], class_=re.compile(r'post|entry|bando'), limit=20):
                try:
                    # Cerca titolo
                    title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    
                    # Cerca link
                    link_elem = article.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else ""
                    
                    # Estrai contenuto per descrizione
                    content = article.get_text()[:1000]
                    
                    # Keyword matching
                    full_text = f"{title} {content}"
                    keyword_match = self.contains_keywords(full_text, keywords)
                    
                    # Aggiungi se rilevante
                    if 'bando' in title.lower() or 'finanziamento' in title.lower() or keyword_match:
                        bandi.append({
                            'title': title[:500],
                            'ente': 'CSV Napoli',
                            'scadenza_raw': '',
                            'link': link,
                            'descrizione': content,
                            'fonte': BandoSource.CSV_SALERNO,
                            'keyword_match': keyword_match or "csv, napoli, terzo settore"
                        })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing CSV Napoli: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping CSV Napoli: {e}")
            
        return bandi
    
    async def scrape_csv_salerno_real(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping CSV Salerno - Sito reale"""
        bandi = []
        try:
            url = "https://www.csvsalerno.it/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca nella homepage e sezioni bandi
            for elem in soup.find_all(['article', 'div', 'section'], limit=30):
                try:
                    text = elem.get_text()
                    if not ('bando' in text.lower() or 'finanziamento' in text.lower()):
                        continue
                    
                    title_elem = elem.find(['h1', 'h2', 'h3', 'h4'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    
                    link_elem = elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else url
                    
                    keyword_match = self.contains_keywords(text, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'CSV Salerno',
                        'scadenza_raw': '',
                        'link': link,
                        'descrizione': text[:1000],
                        'fonte': BandoSource.CSV_SALERNO,
                        'keyword_match': keyword_match or "csv, salerno"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing CSV Salerno: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping CSV Salerno: {e}")
            
        return bandi
    
    async def scrape_csv_assovoce(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping CSV ASSO.VO.CE - Irpinia Sannio"""
        bandi = []
        try:
            url = "https://csvassovoce.it/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca link a bandi
            for link_elem in soup.find_all('a', href=True, limit=50):
                try:
                    href = link_elem.get('href', '')
                    title = link_elem.get_text(strip=True)
                    
                    # Solo link rilevanti per bandi
                    if not title or len(title) < 10:
                        continue
                    
                    if not ('bando' in title.lower() or 'opportunit' in title.lower() or 'finanziamento' in title.lower()):
                        continue
                    
                    full_link = urljoin(url, href)
                    keyword_match = self.contains_keywords(title, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'CSV ASSO.VO.CE Irpinia Sannio',
                        'scadenza_raw': '',
                        'link': full_link,
                        'descrizione': f"Opportunità per il terzo settore in Irpinia e Sannio: {title}",
                        'fonte': BandoSource.CSV_SALERNO,
                        'keyword_match': keyword_match or "irpinia, sannio, volontariato"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing CSV ASSO.VO.CE: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping CSV ASSO.VO.CE: {e}")
            
        return bandi
    
    async def scrape_infobandi_csvnet(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping InfoBandi CSVnet - Portale nazionale CSV"""
        bandi = []
        try:
            url = "https://infobandi.csvnet.it/home/bandi-attivi/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca tutti i link a bandi attivi
            for link_elem in soup.find_all('a', href=True, limit=30):
                try:
                    href = link_elem.get('href', '')
                    title = link_elem.get_text(strip=True)
                    
                    # Solo bandi con titolo significativo
                    if not title or len(title) < 15:
                        continue
                    
                    # Scarta link di navigazione
                    if any(word in title.lower() for word in ['home', 'menu', 'cerca', 'login']):
                        continue
                    
                    full_link = urljoin(url, href)
                    
                    # Cerca scadenza nel parent
                    parent = link_elem.find_parent(['div', 'article', 'li'])
                    scadenza_raw = ""
                    if parent:
                        parent_text = parent.get_text()
                        scadenza_match = re.search(r'scadenza[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})', parent_text, re.I)
                        if scadenza_match:
                            scadenza_raw = scadenza_match.group(1)
                    
                    keyword_match = self.contains_keywords(title, keywords)
                    
                    bandi.append({
                        'title': title[:500],
                        'ente': 'CSVnet Italia',
                        'scadenza_raw': scadenza_raw,
                        'link': full_link,
                        'descrizione': f"Bando nazionale per il terzo settore: {title}",
                        'fonte': BandoSource.FONDAZIONE_COMUNITA,
                        'keyword_match': keyword_match or "csvnet, nazionale, terzo settore"
                    })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing InfoBandi: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping InfoBandi: {e}")
            
        return bandi
    
    async def run_monitoring(self, db: AsyncSession, config: BandoConfig) -> Dict:
        """Esegue il monitoraggio con una configurazione specifica"""
        
        # Crea log di esecuzione
        log_data = {
            'config_id': config.id,
            'started_at': datetime.now(),
            'status': 'running'
        }
        
        all_bandi = []
        new_bandi = 0
        errors = 0
        sources_processed = {}
        
        try:
            # SITI UFFICIALI E SPECIFICI PER BANDI APS SALERNO/CAMPANIA
            sources_to_process = [
                ('fondazione_comunita_salernitana', self.scrape_fondazione_comunita_salernitana),
                ('regione_campania_bandi', self.scrape_regione_campania_bandi),
                ('sviluppo_campania', self.scrape_sviluppo_campania),
                ('fse_regione_campania', self.scrape_fse_regione_campania),
                ('comune_salerno', self.scrape_comune_salerno_real),
                ('arci_servizio_civile', self.scrape_arci_servizio_civile),
                ('csr_campania', self.scrape_csr_campania),
                ('csv_napoli', self.scrape_csv_napoli),
                ('granter_campania', self.scrape_granter_campania),
                ('contributi_regione', self.scrape_contributi_regione_campania)
            ]
            
            # Processa ogni fonte
            for source_name, scrape_func in sources_to_process:
                try:
                    logger.info(f"Processando fonte: {source_name}")
                    bandi_fonte = await scrape_func(config.keywords, config)
                    all_bandi.extend(bandi_fonte)
                    
                    sources_processed[source_name] = {
                        'found': len(bandi_fonte),
                        'processed_at': datetime.now().isoformat(),
                        'status': 'success'
                    }
                    
                    # Delay tra fonti
                    if config.scraping_delay > 0:
                        await asyncio.sleep(config.scraping_delay)
                        
                except Exception as e:
                    errors += 1
                    sources_processed[source_name] = {
                        'found': 0,
                        'error': str(e),
                        'status': 'failed'
                    }
                    logger.error(f"Errore processando {source_name}: {e}")
            
            # Salva i bandi nel database
            for bando_data in all_bandi:
                try:
                    # Controllo duplicati con hash
                    hash_id = self.generate_hash(
                        bando_data['title'], 
                        bando_data['ente'], 
                        bando_data['link']
                    )
                    
                    existing = await bando_crud.get_bando_by_hash(db, hash_id)
                    if not existing:
                        # Parsing data scadenza
                        scadenza_parsed = None
                        if bando_data.get('scadenza_raw'):
                            scadenza_parsed = self.parse_date(bando_data['scadenza_raw'])
                        
                        # Crea nuovo bando
                        new_bando = Bando(
                            title=bando_data['title'],
                            ente=bando_data['ente'],
                            scadenza=scadenza_parsed,
                            scadenza_raw=bando_data.get('scadenza_raw'),
                            link=bando_data['link'],
                            descrizione=bando_data.get('descrizione'),
                            fonte=bando_data['fonte'],
                            hash_identifier=hash_id,
                            keyword_match=bando_data.get('keyword_match'),
                            status=BandoStatus.ATTIVO
                        )
                        
                        db.add(new_bando)
                        new_bandi += 1
                        
                except Exception as e:
                    errors += 1
                    logger.error(f"Errore salvando bando: {e}")
            
            await db.commit()
            
            # Aggiorna config con timestamp
            config.last_run = datetime.now()
            config.next_run = datetime.now() + timedelta(hours=config.schedule_interval_hours)
            await db.commit()
            
            return {
                'status': 'completed',
                'bandi_found': len(all_bandi),
                'bandi_new': new_bandi,
                'errors_count': errors,
                'sources_processed': sources_processed
            }
            
        except Exception as e:
            logger.error(f"Errore generale monitoraggio: {e}")
            return {
                'status': 'failed',
                'bandi_found': len(all_bandi),
                'bandi_new': new_bandi,
                'errors_count': errors + 1,
                'error_message': str(e),
                'sources_processed': sources_processed
            }


# Istanza singleton del servizio
bando_monitor_service = BandoMonitorService()
