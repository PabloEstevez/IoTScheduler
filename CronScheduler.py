from crontab import CronTab
import sys
import os
import pwd
import argparse


## VARS ##

username = pwd.getpwuid(os.getuid())[0]
cron = CronTab(user=username)


## FUNCTIONS ##

def refresh_cron():
    global cron
    cron = CronTab(user=username)

def set_task(command_init, command_final, inicio, duracion, comentario, ott):
    refresh_cron()
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
    if len(inicio.split(" ")[0].split(":")) > 1:
        m = int(inicio.split(" ")[0].split(":")[1])
    else:
        m = 0

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
        command_final += " ; python3 " + __file__ + " --delete " + comentario
    job = cron.new(command=command_final, comment=comentario+"_Final")
    job.setall(m,h,dom,mon,dow)

    cron.write()


def remove_task(id):
    refresh_cron()
    cron.remove_all(comment=id+"_Inicio")
    cron.remove_all(comment=id+"_Final")

    cron.write()


def get_tasks():
    refresh_cron()
    jobs = []
    for job in cron:
        jobs.append(str(job))
    return jobs

## MAIN ##

def main():
    parser = argparse.ArgumentParser(description="Basic automated job scheduler using Python.")
    parser.add_argument("--delete", help="ID of the task to delete.")
    parser.add_argument("--ott", dest="ott", action="store_true", help="One Time Task.")
    parser.add_argument("--set_task", dest="set_task", nargs=5, help="Set a task. Syntax: --set_task <init_command> <end_command> <init_time> <duration> <id>")
    parser.add_argument("--get_tasks", dest="get_tasks", action="store_true", help="Get currently scheduled tasks.")
    parser.set_defaults(ott=False, get_tasks=None)
    args = parser.parse_args()
    if args.delete != None:
        remove_task(args.delete)
    elif args.get_tasks != None:
        get_tasks()
    elif args.set_task != None:
        set_task(args.set_task[0],args.set_task[1],args.set_task[2],int(args.set_task[3]),args.set_task[4], args.ott)
    else:
        set_task(None,None,None,None,None, args.ott)
    

if __name__ == "__main__":
    main()

