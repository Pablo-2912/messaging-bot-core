from enum import Enum


class WorkerLifecycleStatus(str, Enum):
    """
    Representa o estado do ciclo de vida de um worker.
    """

    # O processo do worker NÃO está em execução no sistema operacional.
    STOPPED = "stopped"

    # O processo foi iniciado e o worker está em fase de bootstrap.
    # O processo JÁ existe no SO.
    STARTING = "starting"

    # O processo está em execução no SO e o worker está ativo.
    RUNNING = "running"

    # O processo está em execução no SO e o worker está entrando em pausa.
    PAUSING = "pausing"

    # O processo está em execução no SO, mas o worker está pausado.
    PAUSED = "paused"

    # O worker solicitou encerramento e está em fase de shutdown.
    # O processo AINDA existe no SO.
    STOPPING = "stopping"