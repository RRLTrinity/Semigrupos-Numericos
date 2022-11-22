def GeradorMinimal(dado):#primeira função #cadê o dado?
    dado.sort()#sort.  
    lim=int(dado[-1]/dado[0])+1
    BASE=[0]
    for i in range(len(dado)):
        for h in range(len(BASE)):
            for j in range(lim):
                if BASE[h] + dado[i] * (j + 2)<= dado[-1]:
                    BASE.append(BASE[h] + dado[i] * (j + 2))
    BASE.sort()
    BASE = sorted(set(BASE))
    BASE.remove(0)
    clone=dado[:]
    for i in range(len(BASE)):
        for j in range(len(dado)):
            if BASE[i]==dado[j]:
                clone.remove(dado[j])
    return clone


def SemigrupoNumerico(molde, dado):#segunda função 
    d = dado
    d.sort()
    error = False
    if molde == "Lacunas":

        g = len(dado)
        lim = [i+1 for i in range(2 * g+1)]

        for i in range(g):
            lim.remove(d[i])
        n = len(lim) * lim[0]
        k = 1
        cl=[0]
        for i in range(len(lim)):
            for h in range(k):
                for j in range(n - 1):
                    if (cl[h] + lim[i] * (j + 1)) <= d[-1]:
                        cl.append(cl[h] + lim[i] * (j + 1))
                    else:
                        break

            k = len(cl)
        cl.sort()
        cl = sorted(set(cl))
########
        for i in range(g):
            for j in range(len(cl)):
                if d[i] == cl[j]:
                    print("Lacunas inválidas!")
                    error = True
                    break
            if error:
                break
        if (error):
            return 0
        SN = {"Lacunas": d, "Frobenius": d[g - 1], "Genero": g, "Condutor": d[g - 1] + 1}#####SN
        SN["subcon"] = lim
        SN["Multiplicidade"] = lim[0]
        print("\n\n\nSemigrupo Numérico de gênero ", g, "criado!")
        return SN
    elif molde == "Geradores":
        if d[0] == 1:
            SN = {"Gerador": d[0], "Multiplicidade": d[0], "Genero": 0, "Lacunas": [], "Frobenius": -1, "Condutor": 0}
            SN["subcon"] = [0]
###########
            return SN
        else:
            l = len(d)
            gm= GeradorMinimal(d)
            SN = {"Geradores": d, "Multiplicidade": d[0], "Geradores Minimais":gm}
            print("Semigrupo Numérico criado com ", l, " geradores!\n")
            SN["subcon"] = [0]
            print(SN["Geradores Minimais"])
            PC=2*gm[-1]*int(gm[0]/len(gm))-gm[0]+1
            #n=int(PC/gm[0])
            n = l * SN["Multiplicidade"]
            k = 1
            for i in range(l):
                for h in range(k):
                    for j in range(n-1):
                        if(SN["subcon"][h] + SN["Geradores"][i] * (j + 1))>(PC+d[0]-1):
                            break
                        else:
                            SN["subcon"].append(SN["subcon"][h] + SN["Geradores"][i] * (j + 1))
                k = len(SN["subcon"])
            SN["subcon"].sort()
            SN["subcon"] = sorted(set(SN["subcon"]))
            SN["subcon"].remove(0)
            SN["Apery"] = [0]
            h = SN["Multiplicidade"] - 1
            for i in range(h):
                for j in range(k):
                    if SN["subcon"][j] % SN["Multiplicidade"] == (i + 1):
                        SN["Apery"].append(SN["subcon"][j])
                        break
            SN["Genero"] = 0
            l = len(SN["Apery"]) - 1
            SN["Kunz"] = []
            for i in range(l):
                SN["Kunz"].append(int((SN["Apery"][i + 1] - (i + 1)) / SN["Multiplicidade"]))
                SN["Genero"] += SN["Kunz"][i]

            SN["Lacunas"] = [i + 1 for i in range(2 * SN["Genero"])]
            lacunas = [i + 1 for i in range(2 * SN["Genero"])]
            l = len(SN["subcon"])
            nl = False
            for i in range(2 * SN["Genero"]):
                for j in range(l):
                    if lacunas[i] == SN["subcon"][j]:
                        nl = True
                        break
                if nl == True:
                    SN["Lacunas"].remove(lacunas[i])
                    nl = False
            SN["Condutor"] = SN["Lacunas"][SN["Genero"] - 1] + 1
            SN["Frobenius"] = SN["Lacunas"][SN["Genero"] - 1]

            return SN

def TO(sn):#terceira função (transformada de ordinarização)
    s=sn
    if s["Multiplicidade"] == s["Condutor"]:
        s["NumdeOrd"] = 0
        return s
    else:
        s["Lacunas"].append(s["Multiplicidade"])
        s["Lacunas"].sort()
        s["Lacunas"].remove(s["Lacunas"][sn["Genero"]])
        s["subcon"].remove(s["subcon"][0])
        s["subcon"].append(s["Frobenius"])
        s["subcon"].sort()
        s["Multiplicidade"] = s["subcon"][0]
        s["Frobenius"] = s["Lacunas"][sn["Genero"] - 1]
        return s

def TQO(sn):#quarta função (transformada de quase ordinarização)#para um ponto antes da terceira função 
    s=sn
    if s["Multiplicidade"] == s["Condutor"]:
        s["NumdeQuaseOrd"] = 0

        return s
    elif (s["Multiplicidade"]+1) == s["Lacunas"][-1]:
        s["NumdeQuaseOrd"] = 0

        return s
    else:
        s["Lacunas"].append(s["Multiplicidade"])
        s["Lacunas"].sort()
        s["sub-Frobenius"]=s["Lacunas"][sn["Genero"]-1]
        s["Lacunas"].remove(s["Lacunas"][sn["Genero"]-1])
        s["subcon"].remove(s["subcon"][0])
        s["subcon"].append(s["sub-Frobenius"])
        s["subcon"].sort()
        s["Multiplicidade"] = s["subcon"][0]

        return s

def calcnumord(sn):#quinta função (calcula o número de ordinarização)
    s = sn
    g = sn["Genero"]
    m = sn["Multiplicidade"]
    c = sn["Condutor"]
    cap = []
    if m == c:
        s["NumdeOrd"] = 0
        return s
    else:
        lim = [i + 1 for i in range(g)]

        for i in range(g):
            for j in range(len(sn["subcon"])):
                if lim[i] == sn["subcon"][j]:
                    cap.append(sn["subcon"][j])
        s["NumdeOrd"] = len(cap)
        print("Número de Ordinarização:", s["NumdeOrd"])
        return s

def ordlim(sn,lim, tipo):#ordinarização controlada 
    if tipo=="detalhado":
        print("\n Ordinarização:")
    s = sn
    m = sn["Multiplicidade"]#LAYOUT
    c = sn["Condutor"]

    if m == c:
        s["NumdeOrd"] = 0
        return s
    else:

        for i in range(lim):
            s=TO(s)

            if tipo=="detalhado":
                print("\nr=",(i+1))
                print("Lacunas:", s["Lacunas"],)
                print("Semigrupo Numérico: ",s["subcon"])

        sn["Condutor"]= sn["Frobenius"]+1
    print("\n Novo Semigrupo Numérico\n")

    print("Lacunas:", sn["Lacunas"], "\nCondutor:", sn["Condutor"], "\nFrobenius:",
          sn["Frobenius"], "\nMultiplicidade:", sn["Multiplicidade"], "\nGênero:", sn["Genero"],
          "\nNúmero de Ordinarização:", sn["NumdeOrd"])

    return s

def ordinarizar(sn,tipo):#ordinarização descontrolada 
    if tipo=="detalhado":
        print("\n Ordinarização:")
    s = sn
    g = sn["Genero"]#layout 
    m = sn["Multiplicidade"]
    c = sn["Condutor"]
    cap = []#cap.apend
    if m == c:
        s["NumdeOrd"] = 0
        return s
    else:
        lim = [i + 1 for i in range(g)]

        for i in range(g):
            for j in range(len(sn["subcon"])):
                if lim[i] == sn["subcon"][j]:
                    cap.append(sn["subcon"][j])####cap.apend 
        s["NumdeOrd"] = len(cap)

        for i in range(len(cap)):
            s=TO(s)

            if tipo=="detalhado":
                print("\nr=",(i+1))
                print("Lacunas:", s["Lacunas"],)
                print("Semigrupo Numérico: ",s["subcon"])

    s["Condutor"] = s["subcon"][0]
    base = []
    for i in range(g + 1):
        base.append(g + 1 + i)

    s["Geradores"] = base

    print("\n Novo Semigrupo Numérico\n")

    print("Lacunas:", sn["Lacunas"], "\nGeradores:", sn["Geradores"], "\nCondutor:", sn["Condutor"], "\nFrobenius:",
          sn["Frobenius"], "\nMultiplicidade:", sn["Multiplicidade"], "\nGênero:", sn["Genero"],
          "\nNúmero de Ordinarização:", sn["NumdeOrd"])

    return s

def quaseordinarizar(sn,tipo):#quase ordinarização 
    if tipo=="detalhado":
        print("\n Quase Ordinarização:")
    s = sn
    g = sn["Genero"]
    m = sn["Multiplicidade"]#layout
    c = sn["Condutor"]
    cap = []
    contador=0
    for i in range(g):#condição 
        if m<=sn["Lacunas"][i]:
            contador+=1
    if contador<=1:
        s["NumdeQuaseOrd"] = 0
        return s
    else:
        lim = [i + 1 for i in range(g-1)]

        for i in range(g-1):
            for j in range(len(sn["subcon"])):
                if lim[i] == sn["subcon"][j]:
                    cap.append(sn["subcon"][j])#cap
        s["NumQuaseOrd"] = len(cap)

        for i in range(len(cap)):
            s=TQO(s)#

            if tipo=="detalhado":
                print("\ny=",(i+1))
                print("Lacunas:", s["Lacunas"])
                print("Semigrupo Numérico: ",s["subcon"])

    s["Condutor"] = s["subcon"][0]

    print("\n Novo Semigrupo Numérico\n")

    print("Lacunas:", sn["Lacunas"], "\nCondutor:", sn["Condutor"], "\nFrobenius:",
          sn["Frobenius"], "\nMultiplicidade:", sn["Multiplicidade"], "\nGênero:", sn["Genero"],
          "\nNúmero de Quase Ordinarização:", s["NumQuaseOrd"])

    return s
    
