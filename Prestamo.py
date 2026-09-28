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


def main():
    gc = GestionClientes()
    gp = GestionPrestamos()
    cargar_datos(gc, gp)

    while True:
        print("")
        print("SISTEMA DE PRESTAMOS")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Solicitar prestamo")
        print("4. Ver cronograma")
        print("5. Pagar cuota")
        print("6. Probar metodos")
        print("7. Salir")
        op = input("Opcion: ")

        try:
            if op == "1":
                tipo = input("Tipo (1 Natural / 2 Juridico): ")
                cod = input("ID (ej C003): ")
                nom = input("Nombre: ")
                ema = input("Email: ")
                tel = input("Telefono: ")
                dire = input("Direccion: ")
                if tipo == "1":
                    dni = input("DNI: ")
                    ing = float(input("Ingresos: "))
                    cli = ClienteNatural(cod, nom, ema, tel, dire, dni, ing)
                else:
                    ruc = input("RUC: ")
                    rep = input("Representante: ")
                    cli = ClienteJuridico(cod, nom, ema, tel, dire, ruc, rep)
                gc.registrar(cli)
                print("Cliente registrado: " + str(cli))

            elif op == "2":
                for c in gc.listar():
                    
                    print("[" + c.__class__.__name__ + "] " + str(c) + " | " + repr(c))

            elif op == "3":
                idc = input("ID cliente: ")
                cli = gc.buscar_por_id(idc)
                if cli is None:
                    print("No existe cliente con ese ID.")
                    continue
                cod = input("Codigo prestamo (ej P002): ")
                monto = float(input("Monto: "))
                plazo = int(input("Plazo meses: "))
                tea = float(input("TEA %: "))
                tp = input("Tipo (1 Personal / 2 Vehicular): ")
                if tp == "1":
                    seg = float(input("Seguro %: "))
                    pres = PrestamoPersonal(cod, cli, monto, plazo, tea, seg)
                else:
                    sf = float(input("Seguro fijo mensual: "))
                    mod = input("Modelo: ")
                    pres = PrestamoVehicular(cod, cli, monto, plazo, tea, sf, mod)
                score = int(input("Score (300-850): "))
                ev = EvaluacionCrediticia("EV01", cli, score)
                if ev.evaluar()
                    pres.cambiar_estado("APROBADO")
                    pres.generar_cronograma()
                    gp.registrar(pres)
                    print("APROBADO. Cuota: S/ " + str(pres.calcular_cuota()))
                else:
                    pres.cambiar_estado("RECHAZADO")
                    print("RECHAZADO por score bajo.")

            elif op == "4":
                cod = input("Codigo prestamo: ")
                pres = gp.buscar_por_codigo(cod)
                if pres is None:
                    print("No existe ese prestamo.")
                    continue
               
                print(str(pres) + " | Tipo: " + pres.__class__.__name__)
                for cu in pres.cuotas:
                    print(str(cu))

            elif op == "5":
                cod = input("Codigo prestamo: ")
                pres = gp.buscar_por_codigo(cod)
                if pres is None:
                    print("No existe ese prestamo.")
                    continue
                num = int(input("Numero cuota: "))
                encontrada = None
                for cu in pres.cuotas:
                    if cu.numero == num:
                        encontrada = cu
                if encontrada is None:
                    print("Cuota no valida.")
                elif encontrada.pagada:
                    print("Ya esta pagada.")
                else:
                    monto = float(input("Monto a pagar (Cuota S/ " + str(encontrada.monto) + "): "))
                    pg = Pago("PAG01", "2026-01-15", monto, "Efectivo", encontrada)
                    if pg.procesar():
                        print("Pago OK.")
                    else:
                        print("Monto menor a la cuota.")

            elif op == "6":
                probar_metodos()

            elif op == "7":
                print("Gracias por usar el sistema.")
                break
            else:
                print("Opcion no valida.")

        except ValueError as e:
            print("[Error de dato]: " + str(e))
        except Exception as e:
            print("[Error]: " + str(e))
 class Pago(object):
    def __init__(self, id_pago, fecha, monto, medio, cuota):
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser mayor a cero.")
        self.id_pago = id_pago
        self.fecha = fecha
        self.monto = monto
        self.medio = medio
        self.cuota = cuota

    def procesar(self):
        if self.monto >= self.cuota.monto:
            self.cuota.marcar_pagada()
            return True
        return False

    def __str__(self):
        return "Pago " + str(self.id_pago) + " | S/ " + str(self.monto) + " | " + str(self.medio)


# PRESTAMOS 

class Prestamo(object):
    def __init__(self, codigo, cliente, monto, plazo, tea):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if plazo <= 0:
            raise ValueError("El plazo debe ser mayor a cero.")
        self.codigo = codigo
        self.cliente = cliente
        self.monto = monto
        self.plazo = plazo
        self.tea = tea
        self.estado = "PENDIENTE"
        self.cuotas = []

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def agregar_cuota(self, cuota):
        self.cuotas.append(cuota)

    def calcular_cuota(self):
        tem = (1 + self.tea / 100) ** (1.0 / 12) - 1
        if tem == 0:
            return round(self.monto / self.plazo, 2)
        cuota = (self.monto * tem) / (1 - (1 + tem) ** (-self.plazo))
        return round(cuota, 2)

    def generar_cronograma(self):
        self.cuotas = []
        cuota_valor = self.calcular_cuota()
        tem = (1 + self.tea / 100) ** (1.0 / 12) - 1
        saldo = self.monto
        for i in range(1, self.plazo + 1):
            interes = saldo * tem
            amort = cuota_valor - interes
            saldo = saldo - amort
            fecha = "2026-" + str((i % 12) + 1).zfill(2) + "-15"
            c = Cuota(i, cuota_valor, interes, amort, fecha)
            self.cuotas.append(c)
        return self.cuotas

    def __str__(self):
        return "Prestamo " + str(self.codigo) + " | " + str(self.cliente.nombre) + " | S/ " + str(self.monto) + " | " + str(self.estado)

    def __eq__(self, otro):
        if not isinstance(otro, Prestamo):
            return False
        return self.codigo == otro.codigo

    def __hash__(self):
        return hash(self.codigo)


class PrestamoPersonal(Prestamo):
    def __init__(self, codigo, cliente, monto, plazo, tea, seguro_pct):
        Prestamo.__init__(self, codigo, cliente, monto, plazo, tea)
        self.seguro_pct = seguro_pct

    def calcular_cuota(self):
        base = Prestamo.calcular_cuota(self)
        seguro = self.monto * (self.seguro_pct / 100)
        return round(base + seguro, 2)


class PrestamoVehicular(Prestamo):
    def __init__(self, codigo, cliente, monto, plazo, tea, seguro_fijo, modelo):
        Prestamo.__init__(self, codigo, cliente, monto, plazo, tea)
        self.seguro_fijo = seguro_fijo
        self.modelo = modelo

    def calcular_cuota(self):
        base = Prestamo.calcular_cuota(self)
        return round(base + self.seguro_fijo, 2)


if __name__ == "__main__":
    main()
