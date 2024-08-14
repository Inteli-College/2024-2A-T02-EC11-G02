from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

app = FastAPI()


logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, format='{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}')
logger = logging.getLogger(__name__)

class LogMessage(BaseModel):
    message: str

@app.post("/info/")
async def info_message(log_message: LogMessage):
    """
    Rota para receber mensagens de log e registrar no arquivo 'app.log'.
    """
    try:
        # Registrando a mensagem de log
        logger.info(log_message.message)
        return JSONResponse(status_code=200, content={"message": "Log registrado com sucesso"})
    except Exception as e:
        logging.error(f"Erro ao registrar o log: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erro ao registrar o log"})
    
@app.post("/error/")
async def error_message(log_message: LogMessage):
    """
    Rota para simular um erro e registrar no arquivo 'app.log'.
    """
    try:
        logger.error(log_message)
        return JSONResponse(status_code=200, content={"message": "Log registrado com sucesso"})
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erro ao processar a requisição"})
    
@app.post("/warning/")
async def warning_message(log_message: LogMessage):
    """
    Rota para simular um warning e registrar no arquivo 'app.log'.
    """
    try:
        logger.warning(log_message)
        return JSONResponse(status_code=200, content={"message": "Log registrado com sucesso"})
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erro ao processar a requisição"})

@app.post("/critical/")
async def critical_message(log_message: LogMessage):        
    """
    Rota para simular um erro crítico e registrar no arquivo 'app.log'.
    """
    try:
        logger.critical(log_message)
        return JSONResponse(status_code=200, content={"message": "Log registrado com sucesso"})
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erro ao processar a requisição"})

@app.post("/debug/")
async def debug_message(log_message: LogMessage):
    """
    Rota para simular um debug e registrar no arquivo 'app.log'.
    """
    try:
        logger.debug(log_message)
        return JSONResponse(status_code=200, content={"message": "Log registrado com sucesso"})
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erro ao processar a requisição"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
