import math
import time
import matplotlib.pyplot as plt
import numpy as np

class SimuladorCaidaLibre:
    """
    Simulador de caída libre en Python
    Implementa las mismas fórmulas físicas que la versión JavaScript
    """
    
    def __init__(self):
        # Factores de conversión de unidades (igual que en JS)
        self.factores_conversion = {
            'm': 1,        # Metro (unidad base)
            'ft': 3.28084, # 1 metro = 3.28084 pies
            'cm': 100      # 1 metro = 100 centímetros
        }
        
        # Variables de simulación (valores por defecto)
        self.altura_inicial = 100  # metros
        self.unidad_altura = 'm'   # unidad por defecto
        self.gravedad = 9.8        # m/s²
        self.tiempo = 0            # segundos
        self.en_ejecucion = False  # estado de la simulación
        
        # Datos para el gráfico
        self.tiempos = []
        self.alturas = []
    
    def calcular_tiempo_total(self):
        """
        Calcula el tiempo total de caída usando la fórmula física
        t = √(2h/g) donde h es altura y g es gravedad
        Retorna: tiempo total en segundos
        """
        return math.sqrt(2 * self.altura_inicial / self.gravedad)
    
    def convertir_altura(self, altura_metros, unidad_destino):
        """
        Convierte altura entre diferentes unidades
        Parámetros:
        - altura_metros: altura en metros
        - unidad_destino: unidad a convertir ('m', 'ft', 'cm')
        Retorna: altura convertida
        """
        return altura_metros * self.factores_conversion[unidad_destino]
    
    def calcular_posicion_actual(self, tiempo_actual):
        """
        Calcula la posición (altura) actual del objeto
        usando la ecuación: y = h₀ - ½gt²
        Parámetros:
        - tiempo_actual: tiempo transcurrido en segundos
        Retorna: altura actual en metros
        """
        return max(0, self.altura_inicial - 0.5 * self.gravedad * tiempo_actual ** 2)
    
    def calcular_velocidad_actual(self, tiempo_actual):
        """
        Calcula la velocidad actual del objeto
        usando la ecuación: v = gt
        Parámetros:
        - tiempo_actual: tiempo transcurrido en segundos
        Retorna: velocidad actual en m/s
        """
        return self.gravedad * tiempo_actual
    
    def simular_caida(self, duracion_total=None, intervalo=0.1):
        """
        Ejecuta la simulación de caída libre
        Parámetros:
        - duracion_total: tiempo total de simulación (si None, usa tiempo calculado)
        - intervalo: intervalo entre cálculos en segundos
        """
        if duracion_total is None:
            duracion_total = self.calcular_tiempo_total()
        
        self.en_ejecucion = True
        self.tiempos = []
        self.alturas = []
        
        tiempo_actual = 0
        
        print("Iniciando simulación de caída libre...")
        print(f"Altura inicial: {self.altura_inicial} m")
        print(f"Gravedad: {self.gravedad} m/s²")
        print(f"Tiempo total estimado: {duracion_total:.2f} s")
        print("-" * 50)
        
        while tiempo_actual <= duracion_total and self.en_ejecucion:
            # Calcular posición y velocidad actual
            altura_actual = self.calcular_posicion_actual(tiempo_actual)
            velocidad_actual = self.calcular_velocidad_actual(tiempo_actual)
            
            # Almacenar datos para gráfico
            self.tiempos.append(tiempo_actual)
            self.alturas.append(altura_actual)
            
            # Mostrar datos actuales
            altura_convertida = self.convertir_altura(altura_actual, self.unidad_altura)
            print(f"T: {tiempo_actual:5.2f}s | "
                  f"Altura: {altura_convertida:6.2f} {self.unidad_altura} | "
                  f"Velocidad: {velocidad_actual:6.2f} m/s")
            
            # Verificar si llegó al suelo
            if altura_actual <= 0:
                print("¡El objeto ha llegado al suelo!")
                break
            
            # Esperar intervalo y avanzar tiempo
            time.sleep(intervalo)
            tiempo_actual += intervalo
        
        self.en_ejecucion = False
        print("Simulación finalizada.")
    
    def pausar_simulacion(self):
        """Pausa la simulación en curso"""
        self.en_ejecucion = False
        print("Simulación pausada.")
    
    def reiniciar_simulacion(self):
        """Reinicia la simulación a su estado inicial"""
        self.pausar_simulacion()
        self.tiempo = 0
        self.tiempos = []
        self.alturas = []
        print("Simulación reiniciada.")
    
    def mostrar_formulas(self):
        """Muestra las fórmulas físicas utilizadas"""
        print("\n" + "="*50)
        print("FÓRMULAS DE CAÍDA LIBRE")
        print("="*50)
        print("1. Posición: y = h₀ - ½gt²")
        print("   Donde: y = altura actual")
        print("          h₀ = altura inicial") 
        print("          g = aceleración gravitatoria")
        print("          t = tiempo transcurrido")
        print()
        print("2. Velocidad: v = gt")
        print("   Donde: v = velocidad")
        print("          g = aceleración gravitatoria")
        print("          t = tiempo transcurrido")
        print()
        print("3. Tiempo total: t = √(2h₀/g)")
        print("   Donde: t = tiempo total de caída")
        print("          h₀ = altura inicial")
        print("          g = aceleración gravitatoria")
        print("="*50)
    
    def generar_grafico(self):
        """
        Genera un gráfico de posición vs tiempo usando matplotlib
        Similar al gráfico del canvas en la versión web
        """
        if not self.tiempos:
            print("No hay datos de simulación para graficar.")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.tiempos, self.alturas, 'o-', color='#fdbb2d', linewidth=2, markersize=4, label='Datos de simulación')
        
        # Calcular curva teórica para comparación
        tiempos_teoricos = np.linspace(0, max(self.tiempos), 100)
        alturas_teoricas = [self.calcular_posicion_actual(t) for t in tiempos_teoricos]
        plt.plot(tiempos_teoricos, alturas_teoricas, '--', color='white', alpha=0.7, label='Curva teórica')
        
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Altura (m)')
        plt.title('Simulación de Caída Libre - Posición vs Tiempo')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        # Configurar estilo similar al web
        plt.gca().set_facecolor('#1a2a6c')
        plt.gcf().patch.set_facecolor('#1a2a6c')
        plt.gca().tick_params(colors='white')
        plt.gca().xaxis.label.set_color('white')
        plt.gca().yaxis.label.set_color('white')
        plt.gca().title.set_color('white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        
        plt.show()
    
    def interfaz_consola(self):
        """
        Interfaz de consola para interactuar con el simulador
        """
        while True:
            print("\n" + "="*50)
            print("SIMULADOR DE CAÍDA LIBRE - PYTHON")
            print("="*50)
            print(f"1. Altura actual: {self.altura_inicial} {self.unidad_altura}")
            print(f"2. Gravedad actual: {self.gravedad} m/s²")
            print(f"3. Tiempo total estimado: {self.calcular_tiempo_total():.2f} s")
            print("4. Iniciar simulación")
            print("5. Cambiar altura")
            print("6. Cambiar gravedad")
            print("7. Cambiar unidad de altura")
            print("8. Mostrar fórmulas")
            print("9. Generar gráfico")
            print("0. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == '1':
                print(f"Altura actual: {self.altura_inicial} {self.unidad_altura}")
            
            elif opcion == '2':
                print(f"Gravedad actual: {self.gravedad} m/s²")
            
            elif opcion == '3':
                tiempo_total = self.calcular_tiempo_total()
                print(f"Tiempo total estimado: {tiempo_total:.2f} segundos")
            
            elif opcion == '4':
                self.simular_caida()
                self.generar_grafico()
            
            elif opcion == '5':
                try:
                    nueva_altura = float(input("Ingrese nueva altura: "))
                    if nueva_altura > 0:
                        self.altura_inicial = nueva_altura
                        print(f"Altura cambiada a: {nueva_altura} {self.unidad_altura}")
                    else:
                        print("La altura debe ser mayor que 0.")
                except ValueError:
                    print("Por favor ingrese un número válido.")
            
            elif opcion == '6':
                try:
                    nueva_gravedad = float(input("Ingrese nueva gravedad (m/s²): "))
                    if nueva_gravedad > 0:
                        self.gravedad = nueva_gravedad
                        print(f"Gravedad cambiada a: {nueva_gravedad} m/s²")
                    else:
                        print("La gravedad debe ser mayor que 0.")
                except ValueError:
                    print("Por favor ingrese un número válido.")
            
            elif opcion == '7':
                print("Unidades disponibles:")
                print("m - Metros")
                print("ft - Pies") 
                print("cm - Centímetros")
                nueva_unidad = input("Seleccione unidad: ").lower()
                if nueva_unidad in self.factores_conversion:
                    self.unidad_altura = nueva_unidad
                    print(f"Unidad cambiada a: {nueva_unidad}")
                else:
                    print("Unidad no válida.")
            
            elif opcion == '8':
                self.mostrar_formulas()
            
            elif opcion == '9':
                if self.tiempos:
                    self.generar_grafico()
                else:
                    print("Primero ejecute una simulación para generar el gráfico.")
            
            elif opcion == '0':
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida. Por favor seleccione 0-9.")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del simulador
    simulador = SimuladorCaidaLibre()
    
    # Ejecutar interfaz de consola
    simulador.interfaz_consola()
