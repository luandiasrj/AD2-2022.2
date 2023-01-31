# !/usr/bin/env python
# coding: UTF-8
#
## @package AD2_Tkinter
#
# Calcula o valor futuro de uma aplicação financeira. O programa pode ser
# inicializado através de linha de comando recebendo os argumentos,
# retornando os montantes futuros, juros mensais, diários, etc. além de
# informar o valor do imposto a ser pago.
#
# @author Luan Bernardo Dias
# @since 09/10/2022
# @see https://luandiasrj.github.io/dev/
# 
import getopt
import math
import sys

if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk


## Juros compostos.
#
# É a adição de juros ao capital principal de um empréstimo ou depósito,
# ou em outras palavras, juros sobre juros.
#
# É o resultado do reinvestimento dos juros, ao invés de pagá-lo,
# de tal forma que a taxa no próximo período é calculada
# sobre o principal, mais os juros recebidos previamente.
#
# A função de acumulação mostra como uma unidade monetária
# cresce após o período de tempo.
#
# @param r taxa de juros nominal.
# @param t período de tempo total no qual os juros são aplicados
#           (expressa nas mesmas unidades de tempo de r, usualmente anos).
# @param n frequência de composição (pagamento dos juros), por exemplo,
#           mensal, trimestral ou anual.
# @return juros obtidos no período: (1 + r/n)nt − 1
#
def jc(r: float, t: int, n: int = 1) -> float:
    return (1 + r / float(n)) ** (n * t) - 1


## Converte uma taxa diária para uma taxa anual.
# Em matemática financeira, consideramos 252 dias por ano.
#
# @param d taxa de juros diária.
# @param wd número de dias úteis por ano.
# @return taxa de juros anual dada a taxa diária,
#           na forma de um percentual.
#
def day2year(d: float, wd: int = 252) -> float:
    return 100 * jc(d, wd)


## Converte uma taxa de juros anual para uma taxa mensal.
#
# @param a taxa de juros anual.
# @return taxa de juros mensal dada a taxa anual,
#           na forma de um percentual.
#
def year2month(a: float) -> float:
    return 100 * jc(a, 1.0 / 12.0)


## Calcula log1+r 2 (logaritmo de 2 na base 1 + r).
# Pode ser aproximado por 72/(100 ∗ r).
#
# É usada para calcular o tempo necessário
# para dobrar o principal quando sujeito uma taxa de juros dada.
#
# @param r taxa de juros nominal.
# @return tempo para dobrar o principal.
#
def doublePrincipal(r: float) -> float:
    return math.log(2, 1 + r)


# ... Inclua suas funções aqui ...

## Converte uma taxa de juros mensal para uma taxa diária.
#
# @param m taxa de juros mensal.
# @return taxa de juros diária dada a taxa mensal,
#           na forma de um percentual.
#
def month2day(m: float) -> float:
    return 100 * jc(m, 1.0 / 252)


## Converte a taxa de juros para percentual -> 0.1 = 10.0%.
#
# @param t taxa de juros.
# @return taxa de juros em percentual.
#
def to_percent(t: float) -> float:
    return 100 * t


## Calcula a taxa de juros da poupança levando em consideração a taxa da SELIC.
#
# @param t taxa de juros.
# @return taxa de anual de juros da poupança.
#
def jurospoupanca(t: float) -> float:
    if t * 100 < 8.5:
        return t * 0.7
    else:
        return 0.061675


## Dado o valor presente, calcula o valor futuro levando em consideração a
# taxa e quantidade de meses.
#
# @param capital capital inicial.
# @param taxa taxa de juros.
# @param periodo período de tempo.
# @return valor futuro.
#
def valorfuturo(capital: float, taxa: float, periodo: int) -> float:
    return capital * (1 + taxa) ** periodo


## Calcula o valor do imposto.
#
# @param fv valor futuro.
# @param capital capital inicial.
# @param taxa taxa de juros.
# @return valor em R$ dos impostos a pagar.
#
def imposto(fv: float, capital: float, taxa: float) -> float:
    return (fv - capital) * taxa / 100


## Calcula o valor da futuro da aplicação.
#
# @param capital capital inicial.
# @param taxa taxa de juros.
# @param periodo período de tempo.
# @return valor da aplicação.
#
def aplicacao(capital: float, taxa: float, periodo: int) -> float:
    return capital * (1 + taxa) ** periodo


## Calcula o montante final , imposto , rendimento e
# rentabilidade equivalente.
#
# @param c capital
# @param cdi taxa cdi anual
# @param p taxa poupança anual = 0.70 * selic
# @param t rentabilidade da aplicação em função do CDI
# @param i alíquota do imposto de renda
# @param m meses
# @return
#       - montante da aplicação,
#       - montante poupança,
#       - imposto de renda retido ,
#       - rendimento em m meses (%),
#       - rendimento em m meses ,
#       - rendimento líquido em 1 mês,
#       - rentabilidade para igualar poupança (%) CDI
#
def CDB(c: float, cdi: float, p: float, t: float, i: float,
        m: int = 1) -> float:
    # ... Essa deve ser implementada por você ...
    cdi_calculado = t * cdi
    cdi_com_impostos = t - (t * i / 100)
    cdi_com_impostos_cem_porcento = (1 - (
            1 * i / 100)) * cdi  # Fórmula para gerar número mágico "Apl =
    # Poup ="
    taxamensal = year2month(cdi_calculado / 100) / 100
    valor_aplicacao = valorfuturo(c, taxamensal, m)
    aplicacaocomimposto = valor_aplicacao - imposto(valor_aplicacao, c, i)
    poupanca = valorfuturo(c, year2month(jurospoupanca(p)) / 100, m)
    rendimentocomimposto = (aplicacaocomimposto - poupanca) / c * 100

    cdi_ao_mes = year2month(cdi)
    cdi_ao_dia = month2day(cdi)
    poupanca_ao_ano = jurospoupanca(p) * 100
    poupanca_ao_mes = year2month(jurospoupanca(p))
    rentabilidade_ao_ano = cdi_calculado
    rent_com_imp = cdi_com_impostos * cdi

    apl_poup = aplicacaocomimposto - poupanca
    imposto_val = imposto(valor_aplicacao, c, i)
    rendimento_total_perc = ((aplicacaocomimposto - c) / c * 100)
    apl_equal_poup = (jurospoupanca(p) * 100 / cdi_com_impostos_cem_porcento)

    tempo_poup = (doublePrincipal(jurospoupanca(p)),
                  doublePrincipal(jurospoupanca(p)) * 12)
    tempo_aplic = (doublePrincipal(rent_com_imp / 100),
                   doublePrincipal(rent_com_imp / 100) * 12)

    print("\nCapital = $%.2f" % c * 1)
    print("Taxa Selic = %.2f%%" % to_percent(p))
    print("CDI = %.2f%% ao ano = %.4f%% ao mês = %.6f%% ao dia" % (
        to_percent(cdi), year2month(cdi), month2day(cdi)))
    print("Taxa Poup = %.2f%% ao ano = %.4f%% ao mês" % (
        jurospoupanca(p) * 100, year2month(jurospoupanca(p))))

    print("\nIR = %.1f%%" % i)

    print("\nRentabilidade = %.1f%% CDI = %.2f%%" % (t, cdi_calculado))
    print("Com impostos = %.2f%% CDI = %.2f%%" % (
        cdi_com_impostos, rent_com_imp))

    print("\nMeses = %d" % m)

    print("\nMontante Aplicação = $ %.2f" % aplicacaocomimposto)
    print("Montante Poupança = $%.2f" % poupanca)
    print("Apl - Poup (%d meses) = $%.2f" %
          (m, apl_poup))
    print("Imposto = $%.4f" % imposto_val)
    print("Rendimento em %d meses = %.4f%%" % (
        m, rendimento_total_perc))

    print("\nApl - Poup (%d meses) = %.4f%%" % (m, rendimentocomimposto))
    print("Apl = Poup = %.2f%% CDI" % apl_equal_poup)
    print("Tempo 2 x Poupança = %.2f anos = %.2f meses" % tempo_poup)
    print("Tempo 2 x Aplicação = %.2f anos = %.2f meses" % tempo_aplic)

    # Retorna os valores calculados
    resultados = (cdi_ao_mes, cdi_ao_dia, poupanca_ao_ano, poupanca_ao_mes,
                  rentabilidade_ao_ano, cdi_com_impostos, rent_com_imp,
                  aplicacaocomimposto, poupanca, apl_poup, imposto_val,
                  rendimento_total_perc, rendimentocomimposto, apl_equal_poup,
                  tempo_poup[0], tempo_aplic[0])

    return resultados


## Classe construtora da janela com os campos de entrada Capital, Taxa Selic,
# Taxa CDI etc.
#
class Application(tk.Frame):
    ##
    # Método construtor da classe Tkinter
    #
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    ##
    # Função que desenha a janela principal e seus widgets
    #
    def create_widgets(self):
        espace = 5
        bgclr = 'antiquewhite'
        self.master.title("Cálculo de CDB - AD2 - 2022.2")

        # Criação dos campos de entrada
        texto_titulo = "CDBs, LCIs e LCAs indexadas por\nCertificados de " \
                       "Depósitos Interbancários "
        fonte_titulo = ("Arial", 12, "bold")

        # Make a fieldset with a legend and button inside
        self.fieldset = tk.LabelFrame(self, text=texto_titulo, bg="#CABAA8",
                                      font=fonte_titulo, labelanchor="n")
        self.fieldset.pack(padx=10, pady=10)

        # Make a label for title and pack it into the fieldset frame, top,
        # backgroud color orange and font size and bold
        self.title = tk.Label(self.master, text=texto_titulo,
                              bg="#ff6347", font=fonte_titulo,
                              highlightbackground='lightblue',
                              highlightthickness=5)
        # place the label in the top and center of the fieldset
        self.title.place(relx=0.5, y=30, anchor="center")

        self.title_dummie = tk.Label(self.fieldset, width=50,
                                     background="#CABAA8")
        self.title_dummie.pack(padx=10)

        # Make a frame to hold the fields
        self.fields = tk.Frame(self.fieldset, padx=espace, pady=espace,
                               highlightbackground='lightblue',
                               highlightthickness=5)
        self.fields.pack()

        # Make a frame to hold the radio buttons
        self.radio = tk.Frame(self.fields)
        self.radio.pack(fill=tk.X, side=tk.BOTTOM)
        self.radio['bg'] = bgclr

        # Make a frame to hold the labels
        self.labels = tk.Frame(self.fields)
        self.labels.pack(side=tk.LEFT, padx=espace, pady=espace)

        # Make a frame to hold the spinboxes
        self.spinboxes = tk.Frame(self.fields)
        # Pack the spinboxes to the right of the labels
        self.spinboxes.pack(side=tk.LEFT)

        # Make the row of spinboxes and labels
        self.row1 = tk.Frame(self.spinboxes)
        self.row2 = tk.Frame(self.spinboxes)
        self.row3 = tk.Frame(self.spinboxes)
        self.row4 = tk.Frame(self.spinboxes)
        self.row5 = tk.Frame(self.spinboxes)
        self.row1.pack(fill=tk.X, padx=espace, pady=espace)
        self.row2.pack(fill=tk.X, padx=espace, pady=espace)
        self.row3.pack(fill=tk.X, padx=espace, pady=espace)
        self.row4.pack(fill=tk.X, padx=espace, pady=espace)
        self.row5.pack(fill=tk.X, padx=espace, pady=espace)

        # Make the labels
        self.label1 = tk.Label(self.labels, text="Capital:", anchor='w')
        self.label2 = tk.Label(self.labels, text="Taxa Selic:", anchor='w')
        self.label3 = tk.Label(self.labels, text="Taxa CDI:", anchor='w')
        self.label4 = tk.Label(self.labels, text="Rentabilidade:", anchor='w')
        self.label5 = tk.Label(self.labels, text="Meses:", anchor='w')
        self.label6 = tk.Label(self.label1, text="$", anchor='w')
        self.label7 = tk.Label(self.row2, text="% ano")
        self.label8 = tk.Label(self.row3, text="% ano")
        self.label9 = tk.Label(self.row4, text="% CDI")

        # Default values for the spinboxes
        capital = tk.StringVar()
        capital.set("1000")
        taxa_selic = tk.StringVar()
        taxa_selic.set("13.75")
        taxa_cdi = tk.StringVar()
        taxa_cdi.set("13.65")
        rentabilidade = tk.StringVar()
        rentabilidade.set("100")
        meses = tk.StringVar()
        meses.set("1")

        # Make the spinboxes with default values
        self.spinbox1 = tk.Spinbox(
            self.row1, from_=0, to=1000000000, increment=0.01,
            textvariable=capital, width=12)
        self.spinbox2 = tk.Spinbox(
            self.row2, from_=0, to=1000, increment=0.01,
            textvariable=taxa_selic, width=8)
        self.spinbox3 = tk.Spinbox(
            self.row3, from_=0, to=1000, increment=0.01, textvariable=taxa_cdi,
            width=8)
        self.spinbox4 = tk.Spinbox(
            self.row4, from_=0, to=1000, increment=0.01,
            textvariable=rentabilidade, width=6)
        self.spinbox5 = tk.Spinbox(
            self.row5, from_=0, to=1000, increment=1, textvariable=meses,
            width=6)

        # pack the labels
        self.label1.pack(fill=tk.X, padx=espace, pady=espace)
        self.label2.pack(fill=tk.X, padx=espace, pady=espace)
        self.label3.pack(fill=tk.X, padx=espace, pady=espace)
        self.label4.pack(fill=tk.X, padx=espace, pady=espace)
        self.label5.pack(fill=tk.X, padx=espace, pady=espace)
        self.label6.pack(side=tk.RIGHT)  # $

        # pack the spinboxes
        self.spinbox1.pack(side=tk.LEFT)
        self.spinbox2.pack(side=tk.LEFT)
        self.spinbox3.pack(side=tk.LEFT)
        self.spinbox4.pack(side=tk.LEFT)
        self.spinbox5.pack(side=tk.LEFT)
        self.label7.pack(side=tk.LEFT)  # % ano
        self.label8.pack(side=tk.LEFT)  # % ano
        self.label9.pack(side=tk.LEFT)  # % CDI

        # Make a fieldset with a legend and radio buttons inside
        self.fieldset2 = tk.LabelFrame(self.radio, text="Alíquota IR:")
        self.fieldset2.pack(side=tk.LEFT, padx=espace, pady=espace)

        # Format the fieldset without border and transparent background
        self.fieldset2['bd'] = 0

        # Make a frame to hold the radio buttons
        self.radio = tk.Frame(self.fieldset2)
        self.radio.pack(side=tk.BOTTOM)

        # variables for radio buttons
        self.ir = tk.DoubleVar()
        self.ir.set(0)

        # Make a fieldset with a legend and radio buttons inside

        self.radio1 = tk.Radiobutton(
            self.radio, text="0.0 (LCA ou LCI)", variable=self.ir, value=0,
            anchor='w')
        self.radio2 = tk.Radiobutton(
            self.radio, text="15.0 (acima de 721 dias)", variable=self.ir,
            value=15.0, anchor='w')
        self.radio3 = tk.Radiobutton(
            self.radio, text="17.5 (de 361 até 720 dias)", variable=self.ir,
            value=17.5, anchor='w')
        self.radio4 = tk.Radiobutton(
            self.radio, text="20.0 (de 181 até 360 dias)", variable=self.ir,
            value=20.0, anchor='w')
        self.radio5 = tk.Radiobutton(
            self.radio, text="22.5 (até 180 dias)", variable=self.ir,
            value=22.5, anchor='w')

        # pack the radio buttons

        self.radio1.pack(fill=tk.X, padx=10, pady=espace)
        self.radio2.pack(fill=tk.X, padx=10, pady=espace)
        self.radio3.pack(fill=tk.X, padx=10, pady=espace)
        self.radio4.pack(fill=tk.X, padx=10, pady=espace)
        self.radio5.pack(fill=tk.X, padx=10, pady=espace)

        # Make a button to calculate the results, red text,
        # background #f8fad7, hover color #fadad7
        self.button = tk.Button(
            self.fieldset, text="Calcular", command=self.calculate,
            bg="#f8fad7")
        self.button.pack(side=tk.BOTTOM, padx=espace, pady=espace)

        # Make the button text red
        self.button["fg"] = "red"

        # Make the button groove
        self.button["relief"] = "groove"
        self.button["borderwidth"] = 2

        # Make the button change color when the mouse is over it
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

        # Format all background colors of the window
        self.fields['bg'] = bgclr
        self.fieldset2['bg'] = bgclr
        self.spinboxes['bg'] = bgclr
        self.radio['bg'] = bgclr
        self.labels['bg'] = bgclr
        self.row1['bg'] = bgclr
        self.row2['bg'] = bgclr
        self.row3['bg'] = bgclr
        self.row4['bg'] = bgclr
        self.row5['bg'] = bgclr
        self.label1['bg'] = bgclr
        self.label2['bg'] = bgclr
        self.label3['bg'] = bgclr
        self.label4['bg'] = bgclr
        self.label5['bg'] = bgclr
        self.label6['bg'] = bgclr
        self.label7['bg'] = bgclr
        self.label8['bg'] = bgclr
        self.label9['bg'] = bgclr
        self.radio1['bg'] = bgclr
        self.radio2['bg'] = bgclr
        self.radio3['bg'] = bgclr
        self.radio4['bg'] = bgclr
        self.radio5['bg'] = bgclr
        self.fieldset2['bg'] = bgclr

    ## Muda a cor do botão quando o mouse está em cima dele
    #
    def on_enter(self, event):
        self.button["bg"] = "#fadad7"

    ## Muda a cor do botão quando o mouse sai de cima dele
    #
    def on_leave(self, event):
        self.button["bg"] = "#f8fad7"

    ## Essa função tem como objetivo criar uma nova janela com o resultado
    # dos cálculos de juros solicitados
    #
    def calculate(self):
        font = ("Times", "12", "bold")
        padding_ = 10
        border = 8

        # Minimize the main window
        self.master.withdraw()

        # Get the values from the spinboxes
        valor_investido = float(self.spinbox1.get())
        taxa_selic = float(self.spinbox2.get())
        taxa_cdi = float(self.spinbox3.get())
        rentabilidade = float(self.spinbox4.get())
        meses = int(self.spinbox5.get())

        # Get the value from the radio buttons
        ir = self.ir.get()

        # Calculate the results
        # capital, aplicacao_opt, selic, rentabilidade, imposto_opt, meses
        cdi_ao_mes, cdi_ao_dia, poupanca_ao_ano, poup_ao_mes, rent_ao_ano, \
        rent_com_IR, rent_com_impostos, aplc_com_imp, poup, apl_poup, imp_val, \
        rend_total_perc, rend_com_imp, apl_eq_poup, temp_poup, temp_apli = CDB(
            valor_investido, taxa_cdi * 0.01, taxa_selic * 0.01, rentabilidade,
            ir, meses)

        # Create a new window to show the results
        self.results = tk.Toplevel(self)
        self.results.title("Resultado")

        # Creat 3 containers to hold the results
        cointeiner1 = tk.Frame(self.results, padx=padding_, pady=padding_)
        cointeiner1.pack()
        cointeiner2 = tk.Frame(cointeiner1)
        cointeiner2.pack()
        cointeiner3 = tk.Frame(self.results, padx=padding_, pady=padding_,
                               highlightthickness=border,
                               highlightbackground="red")
        cointeiner3.pack()

        lbl = tk.Label(cointeiner2, text="Capital: $%.2f\nTaxa Selic: %.2f%% "
                                         "ao ano\nCDI: %.2f%% ao ano = %.4f%% "
                                         "ao mês = %.6f%% ao dia\nTaxa "
                                         "Poupança: %.2f%% ao ano = %.4f%% ao "
                                         "mês\n\nIR: %.2f%%\n\nRentabilidade: "
                                         "%.1f%% CDI = %.2f%% ao ano\nCom "
                                         "impostos: %.2f%% CDI = %.2f%% ao "
                                         "ano\n\nMeses: %d" % (
                                             valor_investido, taxa_selic,
                                             taxa_cdi, cdi_ao_mes, cdi_ao_dia,
                                             poupanca_ao_ano, poup_ao_mes,
                                             ir, rentabilidade, rent_ao_ano,
                                             rent_com_IR, rent_com_impostos,
                                             meses),
                       font=font, justify=tk.LEFT)
        lbl["font"] = font
        lbl["highlightthickness"] = border
        lbl["highlightbackground"] = "green"
        lbl["pady"] = padding_
        lbl["padx"] = padding_

        # pack the label left
        lbl.pack(side=tk.LEFT)

        lbl2 = tk.Label(
            cointeiner2, text="Montante Aplicação = $%.2f\nMontante Poupança "
                              "= $%.2f\nApl - Poup (%d meses) = "
                              "$%.2f\nImposto = $%.4f\nRendimento em %d meses "
                              "= %.4f%%" % (aplc_com_imp, poup, meses,
                                            apl_poup, imp_val, meses,
                                            rend_total_perc), font=font,
            justify=tk.LEFT)
        lbl2["font"] = font
        lbl2["highlightthickness"] = border
        lbl2["highlightbackground"] = "blue"
        lbl2["pady"] = padding_
        lbl2["padx"] = padding_

        lbl2.pack(side=tk.LEFT, padx=padding_)

        lbl3 = tk.Label(
            cointeiner3, text="Apl - Poup (%d meses) = %.4f%%\nApl ≍ Poup = "
                              "%.2f%% CDI\nTempo 2 × Poupança = %.2f "
                              "anos\nTempo 2 × Aplicação ≍ %.2f anos" % (
                                  meses, rend_com_imp, apl_eq_poup, temp_poup,
                                  temp_apli),
            font=font, justify=tk.LEFT)
        lbl3["font"] = font
        lbl3.pack()

        # Create a button to return to the main window
        self.button2 = tk.Button(
            self.results, text="Voltar", command=self.back)
        self.button2.pack(padx=padding_, pady=padding_)

        # Listen for the close event
        self.results.protocol("WM_DELETE_WINDOW", self.back)

    ## Função que retorna a janela principal
    #
    def back(self):
        self.results.destroy()
        self.master.deiconify()


app = Application()
# do not allow resizing the GUI
app.master.resizable(False, False)


## Função principal que recebe os parâmetros e chama a função CDB e imprime
# informações na tela.
#   @param c capital inicial.
#   @param cdi taxa cdi anual.
#   @param p taxa poupança anual = 0.70 * selic.
#   @param t rentabilidade da aplicação em função do CDI.
#   @param i alíquota do imposto de renda.
#   @param m meses.
#
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:a:s:i:t:m:h",
                                   ["capital=", "aplicacao=", "selic=",
                                    "imposto=", "rentabilidade=", "meses=",
                                    "help"])
    except getopt.GetoptError as err:
        print(err)
        print("Use --help para obter ajuda.")
        sys.exit(2)
    capital = 0
    aplicacao_opt = 0
    selic = 0
    imposto_opt = 0
    rentabilidade = 0
    meses = 1
    for o, a in opts:
        if o in ("-c", "--capital"):
            capital = float(a)
        elif o in ("-a", "--aplicacao"):
            aplicacao_opt = float(a)
        elif o in ("-s", "--selic"):
            selic = float(a)
        elif o in ("-i", "--imposto"):
            imposto_opt = float(a)
        elif o in ("-t", "--rentabilidade"):
            rentabilidade = float(a)
        elif o in ("-m", "--meses"):
            meses = int(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "opção inválida: " + o
    if capital != 0 and aplicacao_opt != 0 and selic != 0 and imposto_opt != 0 \
            and rentabilidade != 0:
        CDB(capital, aplicacao_opt, selic, rentabilidade, imposto_opt, meses)
    else:
        print("Use --help para obter ajuda.")
        app.mainloop()
        sys.exit()


## Função que imprime ajuda.
#
def usage():
    print(
        "Usage: %s -c [capital] -a [CDI anual] -s [Selic] -i [alíquota IR] -t "
        "[taxa CDI] -m [meses] -h [help]" % sys.argv[0])


if __name__ == "__main__":
    main()
