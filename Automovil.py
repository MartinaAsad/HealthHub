class Automovil:
    ruedas=4

    def __init__(self, color, marca, aceleracion, velocidad):
      self.color=color
      self.marca=marca
      self.aceleracion=aceleracion
      self.velocidad=velocidad

    def acelerar(self):
      self.velocidad+=self.aceleracion
      print('acelero: ',self.velocidad)
  
    def frenar(self):
      self.velocidad-=self.aceleracion
      return self.velocidad
      if self.velocidad<=0:
          #self.velocidad=0
          return 0
      
auto=Automovil("rojo", "toyota", 20, 50)
print(auto.ruedas)
print(f'aceleracion: {auto.aceleracion}')
auto.aceleracion=30
auto.aceleracion
print(auto.acelerar)
print(auto.frenar)
#acelerar:velocidad+aceleracion