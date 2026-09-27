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
        

# EVALUACION

class EvaluacionCrediticia(object):
    def __init__(self, id_eval, cliente, score):
        self.id_eval = id_eval
        self.cliente = cliente
        self.score = score
        self.aprobado = False

    def evaluar(self):
        if self.score >= 650:
            self.aprobado = True
        else:
            self.aprobado = False
        return self.aprobado

    def __str__(self):
        return "Eval " + str(self.id_eval) + " | Score: " + str(self.score) + " | Aprobado: " + str(self.aprobado)


# GESTORES 

class GestionClientes(object):
    def __init__(self):
        self.lista = []

    def registrar(self, cliente):
        self.lista.append(cliente)

    def buscar_por_id(self, id_persona):
        for c in self.lista:
            if c.id_persona == id_persona:
                return c
        return None

    def listar(self):
        return self.lista


class GestionPrestamos(object):
    def __init__(self):
        self.lista = []

    def registrar(self, prestamo):
        self.lista.append(prestamo)

    def buscar_por_codigo(self, codigo):
        for p in self.lista:
            if p.codigo == codigo:
                return p
        return None

    def listar(self):
        return self.lista


# PRUEBAS SIMPLES 

def probar_metodos():
    print("--- Pruebas de negocio ---")
    cli = ClienteNatural("C001", "Juan", "j@x.com", "999", "Av 1", "123", 3000)
    p_base = Prestamo("PB1", cli, 5000, 12, 18.5)
    p_per = PrestamoPersonal("PP1", cli, 5000, 12, 18.5, 0.05)
    assert p_per.calcular_cuota() > p_base.calcular_cuota(), "Personal debe sumar seguro"
    print("1. calcular_cuota personal OK:", p_per.calcular_cuota())

    p_veh = PrestamoVehicular("PV1", cli, 5000, 12, 18.5, 20, "Yaris")
    assert p_veh.calcular_cuota() == round(p_base.calcular_cuota() + 20, 2)
    print("2. calcular_cuota vehicular OK:", p_veh.calcular_cuota())

    p_base.generar_cronograma()
    assert len(p_base.cuotas) == 12, "Debe generar 12 cuotas"
    print("3. generar_cronograma OK:", len(p_base.cuotas), "cuotas")

    c1 = p_base.cuotas[0]
    pago = Pago("PAG1", "2026-01-15", c1.monto, "Efectivo", c1)
    assert pago.procesar() is True and c1.pagada is True
    print("4. procesar pago OK:", c1)

    ev = EvaluacionCrediticia("EV1", cli, 700)
    assert ev.evaluar() is True
    ev2 = EvaluacionCrediticia("EV2", cli, 600)
    assert ev2.evaluar() is False
    print("5. evaluar riesgo OK")

    otro = ClienteNatural("C001", "Otro", "o@x.com", "111", "Av 2", "999", 2000)
    assert cli == otro, "__eq__ debe comparar por id"
    assert hash(cli) == hash(otro)
    print("6. __eq__ y __hash__ OK:", repr(cli))

    print("Todas las pruebas pasaron.")


# MENU 

def cargar_datos(gc, gp):
    c1 = ClienteNatural("C001", "Juan Perez", "juan@gmail.com", "987654321", "Av Lima 123", "71234567", 3500)
    c2 = ClienteJuridico("C002", "Inversiones SAC", "c@inv.com", "014567890", "Av Emp 456", "20123456789", "Carlos Gomez")
    gc.registrar(c1)
    gc.registrar(c2)
    p1 = PrestamoPersonal("P001", c1, 5000, 12, 18.5, 0.05)
    p1.cambiar_estado("APROBADO")
    p1.generar_cronograma()
    gp.registrar(p1)
