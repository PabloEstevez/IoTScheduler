from crontab import CronTab
import sys
import os
import pwd
import argparse


## VARS ##

username = pwd.getpwuid(os.getuid())[0]
cron = CronTab(user=username)


## FUNCTIONS ##

def set_task(command_init, command_final, inicio, duracion, comentario, ott):

    m = h = dom = mon = dow = "*"

    if command_init==None:
        command_init = input("Comando de inicio: ")
    if command_final==None:
        command_final = input("Comando de fin: ")
    if inicio==None:
        inicio = input("Inicio (hh:mm [dd/MM]): ")
    if duracion==None:
        duracion = int(input("Duracion (min): "))
    if comentario==None:
        comentario = input("Comentario: ")

    h = int(inicio.split(" ")[0].split(":")[0])
    m = int(inicio.split(" ")[0].split(":")[1])

    # Day of the month and month are optional
    try:
        dom = inicio.split(" ")[1].split("/")[0]
        mon = inicio.split(" ")[1].split("/")[1]
    except:
        pass
    ##

    job = cron.new(command=command_init, comment=comentario+"_Inicio")
    job.setall(m,h,dom,mon,dow)

    h = int(h + ((m + duracion) / 60)) % 24
    m = (m + duracion) % 60

    if ott == True:
        command_final += " && python " + os.getcwd() + "/" + __file__ + " --delete " + comentario
    job = cron.new(command=command_final, comment=comentario+"_Final")
    job.setall(m,h,dom,mon,dow)

    cron.write()


def remove_task(id):
    cron.remove_all(comment=id+"_Inicio")
    cron.remove_all(comment=id+"_Final")

    cron.write()


## MAIN ##

def main():
    parser = argparse.ArgumentParser(description="Basic automated job scheduler using Python.")
    parser.add_argument("--delete", help="ID of the task to delete.")
    parser.add_argument("--ott", help="OTT=[true/false] One Time Task.")
    args = parser.parse_args()
    if args.delete != None:
        remove_task(args.delete)
    elif args.ott != None:
        if args.ott == "true":
            set_task(None,None,None,None,None, True)
    else:
        set_task(None,None,None,None,None, False)


if __name__ == "__main__":
    main()

