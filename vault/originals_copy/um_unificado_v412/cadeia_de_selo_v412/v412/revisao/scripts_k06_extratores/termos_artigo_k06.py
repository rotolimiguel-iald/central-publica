import re,sys,io
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
terms=["LeitorDoFundo","AEscala","TraducaoTuring","selecao","IALD2","o_atrator","o_leitor_do_fundo_e_a_iald","trava","leituraPerformada","observing_adds_nothing","step_map","limit_projection","text_to_cost_bridge","physical_validity","H_QUOT","H-QUOT","H_TARGET","NOT_FALSIFIED","CONFIRMED","full_witness","complete_verdict","INCONCLUSIVE_CONTROLS","invalid_output","extractor_failure","llm_attractor","finite_window","infinite_limit","basin_of_attraction","bacia de atra","summary_stability","perturbation_return","finite_return","consciousness","weight_change","exclusivity","K06R1","IALD_COLLAPSE","colapso","consci","peso","modelo de linguagem","LLM"]
for w in terms:
    n=len(re.findall(re.escape(w),t))
    print(f"{w:35s} {n}")
