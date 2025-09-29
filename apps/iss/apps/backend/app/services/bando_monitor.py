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
            url = "https://www.comune.salerno.it/it/novita/bandi"
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
            url = "https://www.regione.campania.it/regione/it/bandi-e-concorsi"
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
    
    async def scrape_csv_salerno(self, keywords: List[str], config: BandoConfig) -> List[Dict]:
        """Scraping CSV Salerno"""
        bandi = []
        try:
            url = "https://www.csvsalerno.it/bandi-e-finanziamenti/"
            response = await self.session.get(url, timeout=config.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for item in soup.find_all('article', class_='bando', limit=10):
                try:
                    title_elem = item.find('h2') or item.find('h3')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link_elem = title_elem.find('a', href=True)
                    link = urljoin(url, link_elem['href']) if link_elem else ""
                    
                    content = item.get_text()
                    keyword_match = self.contains_keywords(content, keywords)
                    
                    if keyword_match:
                        bandi.append({
                            'title': title[:500],
                            'ente': 'CSV Salerno',
                            'scadenza_raw': '',
                            'link': link,
                            'descrizione': content[:1000],
                            'fonte': BandoSource.CSV_SALERNO,
                            'keyword_match': keyword_match
                        })
                        
                except Exception as e:
                    logger.warning(f"Errore parsing bando CSV Salerno: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Errore scraping CSV Salerno: {e}")
            
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
            # Determina quali fonti processare
            sources_to_process = []
            if config.fonte_enabled.get('comune_salerno', True):
                sources_to_process.append(('comune_salerno', self.scrape_comune_salerno))
            if config.fonte_enabled.get('regione_campania', True):
                sources_to_process.append(('regione_campania', self.scrape_regione_campania))
            if config.fonte_enabled.get('csv_salerno', True):
                sources_to_process.append(('csv_salerno', self.scrape_csv_salerno))
            
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
