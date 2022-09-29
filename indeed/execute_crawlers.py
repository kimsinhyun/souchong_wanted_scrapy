COOKIE_NUM_LIST= [i for i in range(7)]
WHAT_LIST = ['data','Back-End','Front-End','Network','Game Developer','AI','computer vision','system engineer']
WHAT_LIST = [   #Technical support
                'Computer technician',
                'Computer support technician',
                "Help desk worker",
                "Help desk analyst",
                "Help desk support",
                "Help desk technician",
                "Desktop support specialist",
                "IT support specialist",
                "IT technician",
                "Problem manager",
                "Operations analyst",
                "Technical assistance specialist",
                "Technical specialist",
                "Technical support",
                "Support specialist",
                "Computer operator",
                # Information technology analyst
                "Systems designer",
                "Senior systems analyst",
                "Application support analyst",
                "Systems analyst",
                "IT coordinator",
                "IT manager",
                "Solutions architect",
                # Web,
                "Web designer",
                "Web engineer",
                "Web producers",
                "Web development manager",
                "Web development project manager",
                "UX designer",
                "UI designer",
                "UX/UI researcher",
                "UX/UI specialist",
                "Webmaster",
                "Web producer",
                "Web project manager",
                "Web content manager",
                "Multimedia architect",
                "Web analytics developer",
                "Search engine optimization (SEO) consultant",
                "SEO manager",
                "Internet engineer",
                "Interaction designer",
                "Front-end designer",
                "Front-end developer",
                "Mobile developer",
                "Full-stack developer",
                #Technology sales consultant,
                "Technology manager",
                "Technology assistant",
                "Technology specialist",
                "Technical account manager",
                "IT sales executive",
                "IT sales director",
                "Business systems analyst",
                # Security
                "Security specialist",
                "IT security analyst",
                "Network security engineer",
                "Information security analyst",
                "Information security engineer",
                "Information security manager",
                "Information security consultant",
                "Information security project manager",
                "Information security program manager",
                "Management information director",
                "Cyber security specialist",
                "Cyber security manager",
                "Computer forensic investigator",
                #Database
                "Database developer",
                "Database analyst",
                "Database manager",
                "Database engineer",
                "Database specialist",
                "Database coordinator",
                "Data quality manager",
                "Data modeler",
                "Data scientist",
                "Data architect",
                "Information architect",
                "Computer data scientist",
                #Network
                "Computer network specialist",
                "Computer systems analyst",
                "Computer and information research scientist",
                "Computer and information research manager",
                "Network administrator",
                "Network architect",
                "Network analyst",
                "Network technician",
                "Network operations engineer",
                "Network reliability engineer",
                "Network infrastructure specialist",
                # Software Developer
                "Software engineer",
                "Software architect",
                "Software test engineer",
                "Software development manager",
                "Software development engineer",
                "Artificial intelligence engineer",
                "Application developer",
                "Application designer",
                "Application engineer",
                "DevOps engineer",
                "Computer programmer",
                "Lead programmer",
                "Iteration manager",
                "Frameworks specialist",
                "Game developer",
                #Cloud engineer",
                "Cloud systems engineer",
                "Cloud computing engineer",
                "Cloud architect",
                "Cloud system administrator",
                "Cloud consultant",
                "Cloud services provider",
                "Cloud services developer",
                "Cloud product manager",
                #Information technology leadership
                "Chief information officer (CIO)",
                "Chief technology officer (CTO)",
                "IT manager",
                "IT director",
                "IT project manager",
                "Director of technology",
                "Technical operations officer",
                "Information management systems director",
                "Senior IT consultant",
                "Technical lead",
                "CUDA",
                "JAVA",
                "Python",
                "c++",
                "C language",
                "java spring",
                "hadoop",
                "apache spark",
                "visualization",
                "c#",
                "Deep learning",
                "Machine learning",
                "AI",
                
                ]

import os
import subprocess
from xml.etree.ElementTree import C14NWriterTarget
import psutil

def make_cmd_list(COOKIE_NUM_LIST, WHAT_LIST):
    cmd_list = [f'scrapy crawl indeed -a COOKIE_NUM={COOKIE_NUM_LIST[i%7]} -a WHAT="{WHAT_LIST[i]}"' for i in range(len(WHAT_LIST))]
    return cmd_list

def close_all_chrome_processes():
    PROCNAME = "chrome"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

def run_spider(COOKIE_NUM_LIST, WHAT_LIST, i):
    temp_i = i % 5 
    proc = subprocess.Popen(["scrapy","crawl","indeed","-a",f"COOKIE_NUM={COOKIE_NUM_LIST[temp_i]}","-a",f"WHAT={WHAT_LIST[i]}"])
    return proc

if __name__ == "__main__":
    os.chdir("./indeed/spiders/")

    concurrent_processes = []
    cmd_list = make_cmd_list(COOKIE_NUM_LIST=COOKIE_NUM_LIST, WHAT_LIST=WHAT_LIST)
    print(len(cmd_list))
    print(cmd_list[0])
    for i in range(len(WHAT_LIST)):
    # for i in range(98,len(WHAT_LIST)):
        print(f"{i}th iteration")
        if((i % 7 != 0) or i==0):
            print(f"i : {i}")
            proc = subprocess.Popen(cmd_list[i], shell=True)
            concurrent_processes.append(proc)
        else:
            for p in concurrent_processes:
                p.wait()
            print("Close all Chrome processes")
            close_all_chrome_processes()
            concurrent_processes = []
            
            
        
        


    # for i, proc in enumerate(processes):
    #     print("start process communicate")
    #     processes[i].communicate()
    #     # if(i % 5 == 0):
    #     print("close all Chrome Process")
    #     close_all_chrome_processes()
        
        