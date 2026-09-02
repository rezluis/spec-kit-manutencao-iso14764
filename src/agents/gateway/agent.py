"""
Gateway Agent - Recebe gatilhos, classifica e normaliza solicitações.

Este agente é o ponto de entrada do fluxo de manutenção. Ele:
1. Recebe gatilhos de diversas fontes (arquivos, API, stdin, etc.)
2. Classifica o tipo de manutenção (corretiva, adaptativa, etc.)
3. Extrai informações relevantes (stack trace, issue, etc.)
4. Gera uma solicitação normalizada em JSON
5. Dispara o próximo agente (ou salva para orquestração)
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

import yaml
from pydantic import BaseModel, ValidationError
from structlog import get_logger

# Configurar logging estruturado
logger = get_logger(__name__)


class TriggerSource:
    """Enum para tipos de fonte de gatilho."""
    LOG = "LOG"
    ISSUE = "ISSUE"
    EMAIL = "EMAIL"
    FEATURE_REQUEST = "FEATURE_REQUEST"
    SECURITY_ALERT = "SECURITY_ALERT"
    DEPENDENCY_UPDATE = "DEPENDENCY_UPDATE"
    MANUAL = "MANUAL"


class MaintenanceType:
    """Enum para tipos de manutenção (ISO 14764)."""
    CORRETIVA = "corretiva"
    ADAPTATIVA = "adaptativa"
    PERFECTIVA = "perfectiva"
    PREVENTIVA = "preventiva"


class Priority:
    """Prioridades."""
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"


class NormalizedRequest(BaseModel):
    """Modelo da solicitação normalizada."""
    tipo: MaintenanceType
    prioridade: Priority
    descricao: str
    contexto_adicional: Optional[str] = None
    arquivos_afetados: list[str] = []
    referencias: list[str] = []
    fonte: TriggerSource
    raw_trigger: str
    timestamp: str = datetime.utcnow().isoformat()


class GatewayAgent:
    """
    Agente de entrada para o fluxo de manutenção.
    
    Responsabilidades:
    - Receber gatilhos de múltiplas fontes
    - Classificar e priorizar
    - Normalizar para formato padrão
    - Salvar artefato e disparar próximo agente
    """

    def __init__(self, config_path: Union[str, Path]):
        """
        Inicializa o Gateway Agent com arquivo de configuração.
        
        Args:
            config_path: Caminho para o arquivo YAML de configuração.
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._setup_logging()
        self.work_dir = Path(self.config.get('gateway', {}).get('work_dir', '.gateway_work'))
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar cliente LLM (stub - será implementado com a skill)
        self.llm_client = self._init_llm()
        
        logger.info("GatewayAgent initialized", work_dir=str(self.work_dir))
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
        
        # Substituir variáveis de ambiente ${VAR}
        config = self._resolve_env_vars(raw_config)
        return config
    
    def _resolve_env_vars(self, obj: Any) -> Any:
        """Substitui ${ENV_VAR} por valores do ambiente."""
        if isinstance(obj, dict):
            return {k: self._resolve_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._resolve_env_vars(v) for v in obj]
        elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
            env_var = obj[2:-1]
            return os.getenv(env_var, '')
        else:
            return obj
    
    def _setup_logging(self):
        """Configura logging baseado no arquivo de configuração."""
        log_config = self.config.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        # Configuração simplificada para o exemplo
        logging.basicConfig(level=log_level)
    
    def _init_llm(self):
        """Inicializa o cliente LLM (stub para demonstração)."""
        # Este método será substituído pela skill classify-trigger
        # Aqui retornamos apenas um placeholder
        return {
            "provider": self.config.get('gateway', {}).get('llm', {}).get('provider', 'mock')
        }
    
    def process_trigger(self, trigger_raw: str, source_type: str, metadata: Optional[Dict] = None) -> NormalizedRequest:
        """
        Processa um gatilho bruto e retorna uma solicitação normalizada.
        
        Este é o método principal do Gateway Agent.
        
        Args:
            trigger_raw: Texto bruto do gatilho (log, issue, e-mail, etc.)
            source_type: Fonte do gatilho (ex: 'LOG', 'ISSUE')
            metadata: Dados adicionais (ex: issue_id, stack trace separado)
        
        Returns:
            NormalizedRequest: Solicitação estruturada.
        """
        logger.info("Processing trigger", source=source_type, raw_preview=trigger_raw[:100])
        
        # 1. Classificar tipo de manutenção (usando heurística + LLM)
        maintenance_type = self._classify_type(trigger_raw, source_type)
        
        # 2. Determinar prioridade
        priority = self._determine_priority(trigger_raw, maintenance_type)
        
        # 3. Extrair descrição e contexto
        description, context = self._extract_description_and_context(trigger_raw, metadata)
        
        # 4. Identificar arquivos suspeitos (se houver menção)
        affected_files = self._extract_affected_files(trigger_raw)
        
        # 5. Extrair referências (issue IDs, etc.)
        references = self._extract_references(trigger_raw, metadata)
        
        # 6. Montar solicitação normalizada
        request = NormalizedRequest(
            tipo=maintenance_type,
            prioridade=priority,
            descricao=description,
            contexto_adicional=context,
            arquivos_afetados=affected_files,
            referencias=references,
            fonte=source_type,
            raw_trigger=trigger_raw
        )
        
        # 7. Persistir artefato
        self._save_artefact(request)
        
        # 8. Disparar próximo agente (aqui, somente salvamos; a orquestração virá depois)
        logger.info("Trigger processed successfully", 
                   tipo=request.tipo, 
                   prioridade=request.prioridade)
        
        return request
    
    # --- Métodos auxiliares ---
    
    def _classify_type(self, trigger_raw: str, source_type: str) -> str:
        """
        Classifica o tipo de manutenção com base em heurísticas e LLM.
        
        Aqui usamos uma versão simplificada; em produção, chamaríamos
        a skill `classify-trigger` com um prompt apropriado.
        """
        # Heurística básica
        trigger_lower = trigger_raw.lower()
        if any(kw in trigger_lower for kw in ['exception', 'error', 'fail', 'bug', 'crash']):
            return MaintenanceType.CORRETIVA
        elif any(kw in trigger_lower for kw in ['update', 'upgrade', 'dependency', 'version', 'compatibility']):
            return MaintenanceType.ADAPTATIVA
        elif any(kw in trigger_lower for kw in ['performance', 'optimize', 'refactor', 'improve']):
            return MaintenanceType.PERFECTIVA
        elif any(kw in trigger_lower for kw in ['vulnerability', 'security', 'technical debt']):
            return MaintenanceType.PREVENTIVA
        
        # Fallback para LLM (se disponível)
        if self.llm_client.get('provider') != 'mock':
            return self._classify_with_llm(trigger_raw)
        
        # Se não classificou, assume corretiva (padrão)
        logger.warning("Could not classify trigger, defaulting to corretiva")
        return MaintenanceType.CORRETIVA
    
    def _classify_with_llm(self, trigger_raw: str) -> str:
        """Usa LLM para classificar (stub)."""
        # Implementação futura com chamada à API
        # Por enquanto, retorna corretiva
        return MaintenanceType.CORRETIVA
    
    def _determine_priority(self, trigger_raw: str, maintenance_type: str) -> str:
        """Determina prioridade baseado em regras (ISO-08)."""
        # Regras básicas
        if 'production' in trigger_raw.lower() or 'critical' in trigger_raw.lower():
            return Priority.ALTA
        if maintenance_type in (MaintenanceType.CORRETIVA, MaintenanceType.PREVENTIVA):
            # Corretivas e preventivas têm alta prioridade por padrão
            return Priority.ALTA
        if maintenance_type == MaintenanceType.ADAPTATIVA:
            return Priority.MEDIA
        return Priority.BAIXA
    
    def _extract_description_and_context(self, trigger_raw: str, metadata: Optional[Dict]) -> tuple:
        """Extrai descrição e contexto do trigger."""
        # Se metadata contiver descrição, usar
        if metadata and 'description' in metadata:
            desc = metadata['description']
        else:
            # Gerar uma descrição a partir das primeiras linhas
            lines = trigger_raw.split('\n')
            desc = lines[0][:200] if lines else "No description"
        
        # Contexto adicional: stack trace ou e-mail completo
        context = trigger_raw if len(trigger_raw) > 200 else None
        
        return desc, context
    
    def _extract_affected_files(self, trigger_raw: str) -> list[str]:
        """Tenta identificar arquivos mencionados no trigger."""
        # Buscar padrões de arquivo Java
        import re
        pattern = r'([\w/]+\.java)'
        matches = re.findall(pattern, trigger_raw)
        # Filtrar e retornar únicos
        unique = list(set(matches))
        return unique
    
    def _extract_references(self, trigger_raw: str, metadata: Optional[Dict]) -> list[str]:
        """Extrai referências como issue IDs, IDs de log, etc."""
        refs = []
        if metadata and 'issue_id' in metadata:
            refs.append(f"ISSUE-{metadata['issue_id']}")
        # Buscar padrões como #123
        import re
        issue_matches = re.findall(r'#(\d+)', trigger_raw)
        refs.extend([f"#issue-{m}" for m in issue_matches])
        return refs
    
    def _save_artefact(self, request: NormalizedRequest):
        """Salva a solicitação normalizada como JSON."""
        artefact_path = self.work_dir / f"request_{datetime.utcnow().isoformat().replace(':', '-')}.json"
        with open(artefact_path, 'w') as f:
            json.dump(request.dict(), f, indent=2, default=str)
        logger.info("Artefact saved", path=str(artefact_path))
    
    # --- Métodos para orquestração futura ---
    
    def trigger_flow(self, trigger_raw: str, source_type: str, metadata: Optional[Dict] = None):
        """
        Método de alto nível que processa e inicia o fluxo completo.
        
        Atualmente apenas processa e salva; posteriormente chamará
        o próximo agente (Architecture Understanding ou Impact Analysis).
        """
        request = self.process_trigger(trigger_raw, source_type, metadata)
        # Placeholder para invocar o próximo agente
        # self._invoke_next_agent(request)
        return request


def main():
    """Ponto de entrada para execução direta do agente."""
    # Exemplo de uso
    config_path = Path(__file__).parent / 'config.yaml'
    agent = GatewayAgent(config_path)
    
    # Exemplo de gatilho (log de erro)
    log_example = """2025-06-10 14:28:15.123 ERROR --- [nio-8080-exec-7] c.t.controller.TaskController : Erro ao atualizar tarefa
java.lang.NullPointerException: Cannot invoke "java.time.LocalDate.isAfter(java.time.chrono.ChronoLocalDate)" because "task.getDueDate()" is null
at com.taskmanager.service.TaskService.updateTask(TaskService.java:78)
at com.taskmanager.controller.TaskController.update(TaskController.java:42)
"""
    
    result = agent.trigger_flow(
        trigger_raw=log_example,
        source_type=TriggerSource.LOG,
        metadata={'issue_id': 123}
    )
    
    print("\n=== SOLICITAÇÃO NORMALIZADA ===")
    print(json.dumps(result.dict(), indent=2, default=str))


if __name__ == "__main__":
    main()