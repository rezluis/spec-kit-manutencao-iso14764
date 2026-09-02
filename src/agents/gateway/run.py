#!/usr/bin/env python3
"""
Script de execução do Gateway Agent.

Permite processar um gatilho via linha de comando:
    python run.py --file trigger.txt --source LOG
    python run.py --text "NullPointerException..." --source ISSUE
"""

import argparse
import json
import sys
from pathlib import Path

from agent import GatewayAgent, TriggerSource


def parse_args():
    parser = argparse.ArgumentParser(description="Gateway Agent - Processa gatilhos de manutenção")
    parser.add_argument('--config', type=Path, default='config.yaml',
                        help='Caminho do arquivo de configuração')
    parser.add_argument('--file', type=Path, help='Arquivo contendo o gatilho')
    parser.add_argument('--text', type=str, help='Texto direto do gatilho')
    parser.add_argument('--source', type=str, required=True,
                        choices=['LOG', 'ISSUE', 'EMAIL', 'FEATURE_REQUEST', 'SECURITY_ALERT', 
                                 'DEPENDENCY_UPDATE', 'MANUAL'],
                        help='Fonte do gatilho')
    parser.add_argument('--metadata', type=str, help='JSON com metadados (ex: {"issue_id": 123})')
    parser.add_argument('--output', type=Path, help='Salvar solicitação normalizada em arquivo')
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Ler trigger
    if args.file:
        with open(args.file, 'r') as f:
            trigger_raw = f.read()
    elif args.text:
        trigger_raw = args.text
    else:
        print("Erro: forneça --file ou --text")
        sys.exit(1)
    
    # Metadados
    metadata = {}
    if args.metadata:
        metadata = json.loads(args.metadata)
    
    # Processar
    agent = GatewayAgent(args.config)
    result = agent.trigger_flow(
        trigger_raw=trigger_raw,
        source_type=args.source,
        metadata=metadata
    )
    
    # Saída
    output = json.dumps(result.dict(), indent=2, default=str)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Resultado salvo em {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()