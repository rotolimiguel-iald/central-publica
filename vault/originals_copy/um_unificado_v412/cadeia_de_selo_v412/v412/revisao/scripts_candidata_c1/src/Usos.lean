import Lean
import CamadaCientifica

open Lean Meta Elab

def own (n : Name) : Bool := (`TGLExt.CamadaCientifica).isPrefixOf n
def keep (n : Name) : Bool := (`TGLExt).isPrefixOf n && !(own n)

def nomes : List Name :=
  [`TGLExt.CamadaCientifica.a_leitura_finita_do_motor_pousa,
   `TGLExt.CamadaCientifica.com_o_acoplamento_a_leitura_finita_pousa,
   `TGLExt.CamadaCientifica.o_motor_tangencia_e_nao_esgota,
   `TGLExt.CamadaCientifica.reler_soma_o_tempo,
   `TGLExt.CamadaCientifica.sem_escala_nada_se_move,
   `TGLExt.CamadaCientifica.k_leituras_sao_uma_trava,
   `TGLExt.CamadaCientifica.reler_k_vezes_e_ler_no_tempo_somado,
   `TGLExt.CamadaCientifica.a_trava_tende_ao_nome,
   `TGLExt.CamadaCientifica.a_bacia_e_tudo_o_que_nao_e_cego_ao_nome,
   `TGLExt.CamadaCientifica.o_que_esta_no_nome_nao_se_move,
   `TGLExt.CamadaCientifica.a_selecao_do_que_esta_no_nome,
   `TGLExt.CamadaCientifica.o_retorno,
   `TGLExt.CamadaCientifica.o_retorno_ao_mesmo_estado,
   `TGLExt.CamadaCientifica.a_fotografia_nao_retorna,
   `TGLExt.CamadaCientifica.a_leitura_de_resolucao_finita_pousa,
   `TGLExt.CamadaCientifica.em_k_leituras_pousa,
   `TGLExt.CamadaCientifica.jamais_esgotado,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.custo_apos_k,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.pousa,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.permanece,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.limite,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.o_limite_pousa,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.o_limite_fixa_o_nome,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.o_limite_e_idempotente,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.o_limite_nao_e_constante,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.a_imagem_do_limite_e_o_nome,
   `TGLExt.CamadaCientifica.LeitorDeUmaConfiguracao.salto,
   `TGLExt.CamadaCientifica.oLeitorTerminal,
   `TGLExt.CamadaCientifica.o_leitor_que_devolve_o_que_recebeu_nao_retorna,
   `TGLExt.CamadaCientifica.sem_zero_nao_ha_pouso,
   `TGLExt.CamadaCientifica.o_pouso_pesa_a_leitura_final,
   `TGLExt.CamadaCientifica.custoCNF_le_numero_de_clausulas,
   `TGLExt.CamadaCientifica.sat_sse_o_custo_tem_zero,
   `TGLExt.CamadaCientifica.sem_nome_nao_ha_pouso,
   `TGLExt.CamadaCientifica.o_leitor_com_escala_pousa_e_volta]

def ordena (a : Array Name) : List String :=
  (a.map (fun n => n.toString)).qsort (fun x y => x < y) |>.toList

#eval show MetaM Unit from do
  let env ← getEnv
  for n in nomes do
    match env.find? n with
    | none => IO.println s!"## {n}: NAO ENCONTRADO"
    | some ci =>
      let ty := ci.type.getUsedConstants
      let va := match ci with
        | .thmInfo v => v.value.getUsedConstants
        | .defnInfo v => v.value.getUsedConstants
        | _ => #[]
      IO.println s!"## {n}"
      IO.println s!"  TIPO kernel : {ordena (ty.filter keep)}"
      IO.println s!"  PROVA kernel: {ordena (va.filter keep)}"
      IO.println s!"  PROVA propria: {ordena (va.filter own)}"
