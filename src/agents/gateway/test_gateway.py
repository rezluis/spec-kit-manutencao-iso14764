"""
Testes unitários para o Gateway Agent.
"""

import json
import tempfile
from pathlib import Path

import yaml
from agent import GatewayAgent, TriggerSource, MaintenanceType, Priority


def test_classify_corretiva():
    config = create_mock_config()
    agent = GatewayAgent(config)
    
    trigger = "java.lang.NullPointerException at TaskService.updateTask"
    request = agent.process_trigger(trigger, TriggerSource.LOG)
    assert request.tipo == MaintenanceType.CORRETIVA


def test_classify_adaptativa():
    config = create_mock_config()
    agent = GatewayAgent(config)
    
    trigger = "Atualizar Spring Boot para 3.2.2 devido a vulnerabilidade"
    request = agent.process_trigger(trigger, TriggerSource.DEPENDENCY_UPDATE)
    assert request.tipo == MaintenanceType.ADAPTATIVA


def test_extract_affected_files():
    config = create_mock_config()
    agent = GatewayAgent(config)
    
    trigger = "Erro em TaskService.java linha 78 e TaskController.java linha 42"
    request = agent.process_trigger(trigger, TriggerSource.LOG)
    assert "TaskService.java" in request.arquivos_afetados
    assert "TaskController.java" in request.arquivos_afetados


def test_save_artefact():
    config = create_mock_config()
    agent = GatewayAgent(config)
    
    trigger = "Teste de salvamento"
    request = agent.process_trigger(trigger, TriggerSource.MANUAL)
    
    work_dir = Path(agent.work_dir)
    files = list(work_dir.glob("request_*.json"))
    assert len(files) > 0
    # Limpar
    for f in files:
        f.unlink()


def create_mock_config():
    """Cria um arquivo de configuração temporário para testes."""
    config_data = {
        'gateway': {
            'work_dir': './.test_work/',
            'llm': {'provider': 'mock'}
        },
        'logging': {'level': 'ERROR'}
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        return Path(f.name)