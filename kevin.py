from netmiko import ConnectHandler
from decouple import config
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


MT1 = { #datos para conexión a MK
    'device_type': 'mikrotik_routeros',
    'host':   config('HOSTIP'),
    'username': config('USER'),
    'password': config('PASSWORD'),
}


def searchinfo(comando):
    try:
        net_connect = ConnectHandler(**MT1)
        print("CONEXIÓN EXITOSA")
        #Para hacer comandos de consulta
        output = net_connect.send_command(comando, delay_factor=5)
        return output
    except NetMikoTimeoutException:
        return "Handled timeout exception"
    except AuthenticationException:
        return "AuthenticationException"
    except SSHException:
        return "SSHException"


def setconfig(comando):
    net_connect = ConnectHandler(**MT1)
    print("CONEXIÓN EXITOSA")
    #Para hacer comandos de configuración
    net_connect.enable()
    output = net_connect.send_config_set(comando)
    salida = output.split("\n") #Se divide respuesta obtenido desde MK
    net_connect.save_config()
    net_connect.exit_enable_mode()
    if salida[2]: #Si devuelve alguna respuesta de error
        return jsonify(error=salida[2])  # retorna error
    return jsonify(message='PETICION EXITOSA')  #Si no, retorna restorna respusta


def send_ping():
    with ConnectHandler(**MT1) as net_connect:
        cmd = "ping"
        target_ip = "8.8.8.8"
        count = "30"

        output = net_connect.send_command_timing(
            cmd, strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            "\n", strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            target_ip, strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            count, strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            "\n", strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            "\n", strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            "\n", strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command_timing(
            "\n", strip_prompt=False, strip_command=False
        )
        print(output)