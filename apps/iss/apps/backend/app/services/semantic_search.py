"""
Servizio di ricerca semantica con embedding per bandi ISS
Implementa matching intelligente basato su similarità semantica
"""

import logging
from typing import List, Dict, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession
import json
import pickle
import os
from datetime import datetime

from app.models.bando import Bando
from app.crud.bando import bando_crud

logger = logging.getLogger(__name__)


class SemanticSearchService:
    """Servizio per ricerca semantica avanzata sui bandi"""
    
    def __init__(self):
        # Modello multilinguaggio ottimizzato per italiano
        self.model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.model = None
        self.bando_embeddings = {}
        # Cache locale per embedding
        import os
        cache_dir = os.path.expanduser("~/.cache")
        os.makedirs(cache_dir, exist_ok=True)
        self.embeddings_cache_file = os.path.join(cache_dir, "bando_embeddings.pkl")
        self.last_update = None
        
    async def initialize(self):
        """Inizializza il modello di embedding"""
        try:
            logger.info("🤖 Inizializzazione modello Sentence Transformers...")
            self.model = SentenceTransformer(self.model_name)
            await self._load_cached_embeddings()
            logger.info("✅ Modello AI inizializzato con successo!")
        except Exception as e:
            logger.error(f"❌ Errore inizializzazione AI: {e}")
            raise
    
    def _prepare_bando_text(self, bando: Bando) -> str:
        """Prepara il testo del bando per l'embedding"""
        # Combina tutti i campi testuali rilevanti
        text_parts = []
        
        if bando.title:
            text_parts.append(f"Titolo: {bando.title}")
        
        if bando.descrizione:
            text_parts.append(f"Descrizione: {bando.descrizione}")
        
        if bando.ente:
            text_parts.append(f"Ente: {bando.ente}")
        
        if bando.categoria:
            text_parts.append(f"Categoria: {bando.categoria}")
        
        if bando.fonte:
            text_parts.append(f"Fonte: {bando.fonte}")
        
        if bando.importo:
            text_parts.append(f"Importo: {bando.importo}")
        
        return " ".join(text_parts)
    
    async def generate_embeddings(self, db: AsyncSession, force_refresh: bool = False) -> Dict[int, np.ndarray]:
        """Genera embedding per tutti i bandi nel database"""
        if not self.model:
            await self.initialize()
        
        # Controlla se serve aggiornamento
        if not force_refresh and self.bando_embeddings and self._is_cache_valid():
            return self.bando_embeddings
        
        logger.info("🔄 Generazione embedding per tutti i bandi...")
        
        # Recupera tutti i bandi attivi
        bandi, _ = await bando_crud.get_bandi(db, skip=0, limit=1000)
        
        self.bando_embeddings = {}
        texts = []
        bando_ids = []
        
        for bando in bandi:
            text = self._prepare_bando_text(bando)
            texts.append(text)
            bando_ids.append(bando.id)
        
        if texts:
            # Genera embedding in batch per efficienza
            embeddings = self.model.encode(texts, show_progress_bar=True)
            
            # Salva gli embedding
            for bando_id, embedding in zip(bando_ids, embeddings):
                self.bando_embeddings[bando_id] = embedding
        
        # Salva cache
        await self._save_embeddings_cache()
        self.last_update = datetime.now()
        
        logger.info(f"✅ Generati {len(self.bando_embeddings)} embedding")
        return self.bando_embeddings
    
    async def semantic_search(self, query: str, db: AsyncSession, limit: int = 10, threshold: float = 0.3) -> List[Tuple[Bando, float]]:
        """Ricerca semantica sui bandi"""
        if not self.model:
            await self.initialize()
        
        # Assicurati che gli embedding siano aggiornati
        await self.generate_embeddings(db)
        
        if not self.bando_embeddings:
            return []
        
        # Genera embedding della query
        query_embedding = self.model.encode([query])[0]
        
        # Calcola similarità con tutti i bandi
        similarities = []
        for bando_id, bando_embedding in self.bando_embeddings.items():
            similarity = cosine_similarity([query_embedding], [bando_embedding])[0][0]
            if similarity >= threshold:
                similarities.append((bando_id, similarity))
        
        # Ordina per similarità
        similarities.sort(key=lambda x: x[1], reverse=True)
        similarities = similarities[:limit]
        
        # Recupera i bandi dal database
        results = []
        for bando_id, similarity in similarities:
            bando = await bando_crud.get_bando(db, bando_id=bando_id)
            if bando:
                results.append((bando, similarity))
        
        logger.info(f"🔍 Ricerca semantica '{query}': {len(results)} risultati")
        return results
    
    async def suggest_similar_bandi(self, bando_id: int, db: AsyncSession, limit: int = 5) -> List[Tuple[Bando, float]]:
        """Suggerisce bandi simili basandosi su uno specifico"""
        if not self.bando_embeddings or bando_id not in self.bando_embeddings:
            await self.generate_embeddings(db)
        
        if bando_id not in self.bando_embeddings:
            return []
        
        target_embedding = self.bando_embeddings[bando_id]
        
        # Calcola similarità con tutti gli altri bandi
        similarities = []
        for other_id, other_embedding in self.bando_embeddings.items():
            if other_id != bando_id:
                similarity = cosine_similarity([target_embedding], [other_embedding])[0][0]
                similarities.append((other_id, similarity))
        
        # Ordina e prendi i top
        similarities.sort(key=lambda x: x[1], reverse=True)
        similarities = similarities[:limit]
        
        # Recupera bandi
        results = []
        for other_id, similarity in similarities:
            bando = await bando_crud.get_bando(db, bando_id=other_id)
            if bando:
                results.append((bando, similarity))
        
        return results
    
    async def match_profile_to_bandi(self, profile: Dict, db: AsyncSession, limit: int = 10) -> List[Tuple[Bando, float]]:
        """Match automatico profilo utente con bandi rilevanti"""
        # Costruisci query semantica dal profilo
        query_parts = []
        
        if profile.get('organization_type'):
            query_parts.append(f"organizzazione {profile['organization_type']}")
        
        if profile.get('sectors'):
            query_parts.append(f"settori: {', '.join(profile['sectors'])}")
        
        if profile.get('target_groups'):
            query_parts.append(f"target: {', '.join(profile['target_groups'])}")
        
        if profile.get('keywords'):
            query_parts.append(f"interesse: {', '.join(profile['keywords'])}")
        
        if profile.get('geographical_area'):
            query_parts.append(f"zona: {profile['geographical_area']}")
        
        query = " ".join(query_parts)
        
        logger.info(f"🎯 Match profilo: '{query}'")
        return await self.semantic_search(query, db, limit=limit, threshold=0.2)
    
    def get_intelligent_suggestions(self, search_history: List[str], limit: int = 5) -> List[str]:
        """Genera suggerimenti intelligenti basati sullo storico"""
        if not search_history or not self.model:
            return self._get_default_suggestions()
        
        # Analizza le query passate per pattern
        recent_queries = search_history[-10:]  # Ultime 10 ricerche
        
        suggestions = []
        
        # Suggerimenti basati su parole chiave frequenti
        keywords_freq = {}
        for query in recent_queries:
            words = query.lower().split()
            for word in words:
                if len(word) > 3:  # Solo parole significative
                    keywords_freq[word] = keywords_freq.get(word, 0) + 1
        
        # Genera suggerimenti intelligenti
        top_keywords = sorted(keywords_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for keyword, _ in top_keywords:
            suggestions.extend([
                f"{keyword} giovani",
                f"{keyword} formazione",
                f"{keyword} digitale",
                f"{keyword} sociale"
            ])
        
        # Rimuovi duplicati e limita
        suggestions = list(set(suggestions))[:limit]
        
        # Se pochi suggerimenti, aggiungi quelli di default
        if len(suggestions) < limit:
            suggestions.extend(self._get_default_suggestions())
        
        return suggestions[:limit]
    
    def _get_default_suggestions(self) -> List[str]:
        """Suggerimenti di default per APS campane"""
        return [
            "progetti sociali giovani",
            "inclusione digitale anziani", 
            "formazione professionale",
            "volontariato culturale",
            "startup sociale",
            "ambiente territorio",
            "cooperazione sociale",
            "innovazione terzo settore"
        ]
    
    async def _load_cached_embeddings(self):
        """Carica embedding dalla cache"""
        try:
            if os.path.exists(self.embeddings_cache_file):
                with open(self.embeddings_cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.bando_embeddings = cache_data.get('embeddings', {})
                    self.last_update = cache_data.get('last_update')
                logger.info(f"📚 Caricati {len(self.bando_embeddings)} embedding da cache")
        except Exception as e:
            logger.warning(f"⚠️ Errore caricamento cache embedding: {e}")
            self.bando_embeddings = {}
    
    async def _save_embeddings_cache(self):
        """Salva embedding nella cache"""
        try:
            cache_data = {
                'embeddings': self.bando_embeddings,
                'last_update': datetime.now()
            }
            with open(self.embeddings_cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        except Exception as e:
            logger.warning(f"⚠️ Errore salvataggio cache embedding: {e}")
    
    def _is_cache_valid(self) -> bool:
        """Controlla se la cache è ancora valida (24 ore)"""
        if not self.last_update:
            return False
        
        hours_passed = (datetime.now() - self.last_update).total_seconds() / 3600
        return hours_passed < 24


# Singleton service instance
semantic_search_service = SemanticSearchService()
