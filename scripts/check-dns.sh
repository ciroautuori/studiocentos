#!/bin/bash

echo "🌐 Verifica DNS per innovazionesocialesalernitana.it"
echo "=================================================="

TARGET_IP="34.22.155.33"
DOMAIN="innovazionesocialesalernitana.it"

# Verifica DNS
echo "Verificando DNS..."
CURRENT_IP=$(curl -s "https://dns.google/resolve?name=$DOMAIN&type=A" | grep -o '"data":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ "$CURRENT_IP" = "$TARGET_IP" ]; then
    echo "✅ DNS configurato correttamente!"
    echo "   $DOMAIN -> $TARGET_IP"
    echo ""
    echo "🔥 Ora puoi accedere a:"
    echo "   https://$DOMAIN"
    echo "   https://admin.$DOMAIN"
    echo ""
    echo "SSL Let's Encrypt si attiverà automaticamente al primo accesso HTTPS."
else
    if [ -z "$CURRENT_IP" ]; then
        echo "❌ DNS NON configurato"
        echo "   $DOMAIN -> nessun record A trovato"
    else
        echo "❌ DNS configurato su IP sbagliato"
        echo "   $DOMAIN -> $CURRENT_IP (dovrebbe essere $TARGET_IP)"
    fi
    echo ""
    echo "🔧 CONFIGURA QUESTI RECORD DNS:"
    echo "================================"
    echo "Tipo: A"
    echo "Nome: @"
    echo "Valore: $TARGET_IP"
    echo "TTL: 300"
    echo ""
    echo "Tipo: A"
    echo "Nome: admin"
    echo "Valore: $TARGET_IP"
    echo "TTL: 300"
fi
