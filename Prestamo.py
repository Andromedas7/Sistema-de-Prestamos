# Sistema de Prestamos - Trabajo Parcial Fundamentos 2

# PERSONAS  

class Persona(object):
    
    def __init__(self, id_persona, nombre, email, telefono):
        self.id_persona = id_persona
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return str(self.id_persona) + " - " + str(self.nombre)

    def __repr__(self):
        return "Persona('" + str(self.id_persona) + "','" + str(self.nombre) + "')"

    def __eq__(self, otro):
        if not isinstance(otro, Persona):
            return False
        return self.id_persona == otro.id_persona

    def __hash__(self):
        return hash(self.id_persona)


class Cliente(Persona):
    
    def __init__(self, id_persona, nombre, email, telefono, direccion):
        Persona.__init__(self, id_persona, nombre, email, telefono)
        self.direccion = direccion

    def __str__(self):
        return Persona.__str__(self) + " | Dir: " + str(self.direccion)


class ClienteNatural(Cliente):
    def __init__(self, id_persona, nombre, email, telefono, direccion, dni, ingresos):
        Cliente.__init__(self, id_persona, nombre, email, telefono, direccion)
        if ingresos <= 0:
            raise ValueError("Los ingresos deben ser mayores a cero.")
        self.dni = dni
        self.ingresos = ingresos

    def __str__(self):
        return Cliente.__str__(self) + " | DNI: " + str(self.dni)

    def __repr__(self):
        return "ClienteNatural('" + str(self.id_persona) + "','" + str(self.nombre) + "')"


class ClienteJuridico(Cliente):
    def __init__(self, id_persona, nombre, email, telefono, direccion, ruc, representante):
        Cliente.__init__(self, id_persona, nombre, email, telefono, direccion)
        self.ruc = ruc
        self.representante = representante

    def __str__(self):
        return Cliente.__str__(self) + " | RUC: " + str(self.ruc)

    def __repr__(self):
        return "ClienteJuridico('" + str(self.id_persona) + "','" + str(self.nombre) + "')"


# CUOTA Y PAGO

class Cuota(object):
    def __init__(self, numero, monto, interes, amortizacion, fecha):
        self.numero = numero
        self.monto = round(monto, 2)
        self.interes = round(interes, 2)
        self.amortizacion = round(amortizacion, 2)
        self.fecha = fecha
        self.pagada = False

    def marcar_pagada(self):
        self.pagada = True

    def __str__(self):
        if self.pagada:
            estado = "PAGADO"
        else:
            estado = "PENDIENTE"
        return "Cuota " + str(self.numero) + " | S/ " + str(self.monto) + " | " + estado

    def __repr__(self):
        return "Cuota(" + str(self.numero) + "," + str(self.monto) + ")"

    def __eq__(self, otro):
        if not isinstance(otro, Cuota):
            return False
        return self.numero == otro.numero and self.monto == otro.monto

    def __hash__(self):
        return hash((self.numero, self.monto))


