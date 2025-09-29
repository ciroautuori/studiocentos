#!/bin/bash

echo "🌐 Configurazione DNS per innovazionesocialesalernitana.it"
echo "========================================================"

SERVER_IP="34.22.155.33"

# Verifica se il dominio punta già al server
echo "Verificando DNS attuale..."
CURRENT_IP=$(curl -s "https://dns.google/resolve?name=innovazionesocialesalernitana.it&type=A" | grep -o '"data":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ "$CURRENT_IP" = "$SERVER_IP" ]; then
    echo "✅ DNS già configurato correttamente!"
    echo "   innovazionesocialesalernitana.it -> $SERVER_IP"
else
    echo "⚠️  DNS non configurato o non propagato"
    echo "   Attuale: $CURRENT_IP"
    echo "   Richiesto: $SERVER_IP"
    echo ""
    echo "CONFIGURA QUESTI RECORD DNS:"
    echo "================================"
    echo "Tipo: A"
    echo "Nome: @"
    echo "Valore: $SERVER_IP"
    echo "TTL: 300"
    echo ""
    echo "Tipo: A"
    echo "Nome: admin"
    echo "Valore: $SERVER_IP"
    echo "TTL: 300"
    echo ""
    echo "Tipo: A"
    echo "Nome: www"
    echo "Valore: $SERVER_IP"
    echo "TTL: 300"
fi
