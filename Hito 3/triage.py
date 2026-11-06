#Lógica para calcular el nivel de triage 

TIEMPOS = {
    "I":   "Requiere atención médica inmediata.",
    "II":  "Requiere atención médica en un tiempo menor a 30 minutos.",
    "III": "Requiere atención médica en un tiempo menor a 60 minutos.",
    "IV":  "Requiere atención médica en un tiempo menor a 120 minutos.",
    "V":   "Requiere atención médica en un tiempo menor a 240 minutos.",
}

def calcular_nivel(respuestas):
    def si (clave):
        return respuestas.get(clave) == "Sí"

    if si("conciencia"):
        return "I", "Alteración del estado de conciencia."
    if si("sangrado") and si("disnea"):
            return "I", "Sangrado activo con dificultad para respirar."
    if si("sangrado"):
                return "II", "Sangrado activo o incontrolable."
    if si("disnea") and si("dolor"):
                    return "II", "Dificultad para respirar con dolor muy intenso."
    if si("disnea"):
            return "III", "Dificultad para respirar."
    if si("dolor"):
            return "III", "Dolor muy intenso."
    if si("fiebre"):
            return "IV", "Fiebre sin signos de alarma."
    return "V", "Sin signos de alarma."
    
    
    