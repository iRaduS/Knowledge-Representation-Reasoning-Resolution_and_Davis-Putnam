import os
import json
import streamlit as st
import subprocess
from enum import Enum

def convert_from_text_fol_to_subarrays(contents):
	if len(contents) == 0:
		return "[]."

	fol_array = []
	
	disjunctions = contents.split(" and ")
	for disjunction in disjunctions:
		clause_array = []
		literals = disjunction.split(" or ")
		for literal in literals:
			current_literal = literal.strip('() ')
			if "(" in current_literal:
				current_literal += ")"
			if current_literal[0] == "~":
				current_literal = f"n({current_literal.strip('~')})"
			clause_array.append(current_literal)
		fol_array.append(clause_array)

	fol = json.dumps(fol_array)
	fol += "."
	fol = fol.replace("\"", "")
	return fol

class PrologProcedureEnum(Enum):
	RESOLUTION_FOL = "resolution_fol"
	RESOLUTION_PROPOSITIONAL = "resolution_propositional"
	DAVIS_PUTNAM_MOST_FREQUENT = "davis_putnam_most_frequent"
	DAVIS_PUTNAM_SHORTEST = "davis_putnam_shortest_clause"

def submit_to_prolog_subprocess(contents, procedure, convert_from_text_to_subarrays=False):
	kb_file_name = os.getcwd() + "/KB.txt"

	if convert_from_text_to_subarrays:
		contents = convert_from_text_fol_to_subarrays(contents)

	with open(kb_file_name, "w") as kb_file:
		kb_file.write(f'{contents}')

	result = subprocess.run(["swipl", "-q", "-t", f"{procedure.value}('{kb_file_name}').", "-s", f"{os.getcwd()}/project.pl"], capture_output=True, text=True)
	st.session_state["prolog_output"] = result.stdout

def resolution_fol_streamlit_page():
	if "prolog_output" not in st.session_state:
		st.session_state["prolog_output"] = ""
	
	st.title("Resolution FOL Application")
	first_example_col, second_example_col, third_example_col = st.columns(3)

	with first_example_col:
		st.header("C3, pg. 30 - example")
		first_example_text = st.text_area("The three-block problem", "[[n(on(X, Y)), n(green(X)), green(Y)], [on(a, b)], [on(b, c)], [green(a)], [n(green(c))]].", disabled=True)
		run_first_example_button = st.button("Run example", key="resolution-fol-first-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(first_example_text, PrologProcedureEnum.RESOLUTION_FOL,))

	with second_example_col:
		st.header("C3, pg. 33 - example")
		second_example_text = st.text_area("The plus and succ problem", "[[plus(0, X, X)], [n(plus(X, Y, Z)), plus(succ(X), Y, succ(Z))], [n(plus(succ(succ(0)), succ(succ(succ(0))), U))]].", disabled=True)
		run_second_example_button = st.button("Run example", key="resolution-fol-second-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(second_example_text, PrologProcedureEnum.RESOLUTION_FOL,))

	with third_example_col:
		st.header("C4, pg. 12 - example")
		third_example_text = st.text_area("The hownd-howl problem", "[[n(hound(X)), howl(X)], [n(have(X, Y)), n(cat(Y)), n(have(X, Z)), n(mouse(Z))], [n(ls(X)), n(have(X, Y)), n(howl(Y))], [have(john, a)], [cat(a), hound(a)], [ls(john)], [have(john, b)], [mouse(b)]].", disabled=True)
		run_third_example_button = st.button("Run example", key="resolution-fol-third-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(third_example_text, PrologProcedureEnum.RESOLUTION_FOL))

	st.header("Custom Input")
	custom_example_input = st.text_area("Custom Input", "(~adult(X) or ~legoSet(Y) or playsWith(X, Y)) and (~legoSet(Y) or ~playsWith(X, Y) or ~techFanatic(X)) and (~usesSmartphone(X) or techFanatic(X)) and (~buysSmartphone(X) or cravesSmartphone(X) or usesSmartphone(X)) and buysSmartphone(paul) and legoSet(dvs) and adult(paul) and ~cravesSmartphone(paul)", placeholder="For negation of a symbol please use ~.")
	run_custom_input_button = st.button("Run custom input", key="resolution-fol-run-custom-button", icon=":material/arrow_forward_ios:", type="primary", on_click=submit_to_prolog_subprocess, args=(custom_example_input, PrologProcedureEnum.RESOLUTION_FOL, True,))

	st.header("SWI-Prolog Output")
	output_text_area = st.text_area("SWI-Prolog Output", st.session_state["prolog_output"], disabled=True, placeholder="Here will be displayed the output of the prolog program.")

def resolution_propositional_streamlit_page():
	if "prolog_output" not in st.session_state:
		st.session_state["prolog_output"] = ""

	st.title("Resolution Propositional Application")
	first_example_col, second_example_col, third_example_col, fourth_example_col = st.columns(4)

	with first_example_col:
		first_example_text = st.text_area("Example #1", "[[n(a), b], [c, d], [n(d), b], [n(b)], [n(c), b], [e], [f, a, b, n(f)]].", disabled=True)
		run_first_example_button = st.button("Run example", key="resolution-prop-first-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(first_example_text, PrologProcedureEnum.RESOLUTION_PROPOSITIONAL,))

	with second_example_col:
		second_example_text = st.text_area("Example #2", "[[n(b), a], [n(a), b, e], [a, n(e)], [n(a)], [e]].", disabled=True)
		run_second_example_button = st.button("Run example", key="resolution-prop-second-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(second_example_text, PrologProcedureEnum.RESOLUTION_PROPOSITIONAL,))

	with third_example_col:
		third_example_text = st.text_area("Example #3", "[[n(a), b], [c, f], [n(c)], [n(f), b], [n(c), b]].", disabled=True)
		run_third_example_button = st.button("Run example", key="resolution-prop-third-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(third_example_text, PrologProcedureEnum.RESOLUTION_PROPOSITIONAL,))

	with fourth_example_col:
		fourth_example_text = st.text_area("Example #4", "[[a, b], [n(a), n(b)], [c]].", disabled=True)
		run_fourth_example_button = st.button("Run example", key="resolution-prop-fourth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(fourth_example_text, PrologProcedureEnum.RESOLUTION_PROPOSITIONAL,))

	st.header("Custom Input")
	custom_example_input = st.text_area("Custom Input", "(a or b) and (~a or ~b) and c", placeholder="For negation of a symbol please use ~.")
	run_custom_input_button = st.button("Run custom input", key="resolution-prop-run-custom-button", icon=":material/arrow_forward_ios:", type="primary", on_click=submit_to_prolog_subprocess, args=(custom_example_input, PrologProcedureEnum.RESOLUTION_PROPOSITIONAL, True,))

	st.header("SWI-Prolog Output")
	output_text_area = st.text_area("SWI-Prolog Output", st.session_state["prolog_output"], disabled=True, placeholder="Here will be displayed the output of the prolog program.")


def davis_putnam_most_frequent_page():
	if "prolog_output" not in st.session_state:
		st.session_state["prolog_output"] = ""

	st.title("Davis Putnam - Most Frequent Strategy")
	first_example_col, second_example_col, third_example_col = st.columns(3)
	with first_example_col:
		first_example_text = st.text_area("Example #1", "[[toddler], [n(toddler), child], [n(child), n(male), boy], [n(infant), child], [n(child), n(female), girl], [female], [girl]].", disabled=True)
		run_first_example_button = st.button("Run example", key="dp-most-frequent-prop-first-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(first_example_text, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT,))

	with second_example_col:
		second_example_text = st.text_area("Example #2", "[[toddler], [n(toddler), child], [n(child), n(male), boy], [n(infant), child], [n(child), n(female), girl], [female], [n(girl)]].", disabled=True)
		run_second_example_button = st.button("Run example", key="dp-most-frequent-prop-second-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(second_example_text, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT,))

	with third_example_col:
		third_example_text = st.text_area("Example #3", "[[n(a), b], [c, d], [n(d), b], [n(b)], [n(c), b], [e], [f, a, b, n(f)]].", disabled=True)
		run_third_example_button = st.button("Run example", key="dp-most-frequent-prop-third-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(third_example_text, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT,))

	fourth_example_col, fifth_example_col, sixth_example_col = st.columns(3)
	with fourth_example_col:
		fourth_example_text = st.text_area("Example #4", "[[n(b), a], [n(a), b, e], [a, n(e)], [n(a)], [e]].", disabled=True)
		run_fourth_example_button = st.button("Run example", key="dp-most-frequent-prop-fourth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(fourth_example_text, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT,))

	with fifth_example_col:
		fifth_example_text = st.text_area("Example #5", "[[n(a), n(e), b], [n(d), e, n(b)], [n(e), f, n(b)], [f, n(a), e], [e, f, n(b)]].", disabled=True)
		run_fifth_example_button = st.button("Run example", key="dp-most-frequent-prop-fifth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(fifth_example_text, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT,))

	with sixth_example_col:
		sixth_example_text = st.text_area("Example #6", "[[a, b], [n(a), n(b)], [n(a), b], [a, n(b)]].", disabled=True)
		run_sixth_example_button = st.button("Run example", key="dp-most-frequent-prop-sixth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(sixth_example_text, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT,))

	st.header("Custom Input")
	custom_example_input = st.text_area("Custom Input", "(a or b) and (~a or ~b) and c", placeholder="For negation of a symbol please use ~.")
	run_custom_input_button = st.button("Run custom input", key="dp-most-frequent-run-custom-button", icon=":material/arrow_forward_ios:", type="primary", on_click=submit_to_prolog_subprocess, args=(custom_example_input, PrologProcedureEnum.DAVIS_PUTNAM_MOST_FREQUENT, True,))

	st.header("SWI-Prolog Output")
	output_text_area = st.text_area("SWI-Prolog Output", st.session_state["prolog_output"], disabled=True, placeholder="Here will be displayed the output of the prolog program.")

def davis_putnam_short_clause_page():
	if "prolog_output" not in st.session_state:
		st.session_state["prolog_output"] = ""

	st.title("Davis Putnam - Shortest Clause Strategy")
	first_example_col, second_example_col, third_example_col = st.columns(3)
	with first_example_col:
		first_example_text = st.text_area("Example #1", "[[toddler], [n(toddler), child], [n(child), n(male), boy], [n(infant), child], [n(child), n(female), girl], [female], [girl]].", disabled=True)
		run_first_example_button = st.button("Run example", key="dp-shortest-clause-prop-first-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(first_example_text, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST,))

	with second_example_col:
		second_example_text = st.text_area("Example #2", "[[toddler], [n(toddler), child], [n(child), n(male), boy], [n(infant), child], [n(child), n(female), girl], [female], [n(girl)]].", disabled=True)
		run_second_example_button = st.button("Run example", key="dp-shortest-clause-prop-second-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(second_example_text, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST,))

	with third_example_col:
		third_example_text = st.text_area("Example #3", "[[n(a), b], [c, d], [n(d), b], [n(b)], [n(c), b], [e], [f, a, b, n(f)]].", disabled=True)
		run_third_example_button = st.button("Run example", key="dp-shortest-clause-prop-third-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(third_example_text, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST,))

	fourth_example_col, fifth_example_col, sixth_example_col = st.columns(3)
	with fourth_example_col:
		fourth_example_text = st.text_area("Example #4", "[[n(b), a], [n(a), b, e], [a, n(e)], [n(a)], [e]].", disabled=True)
		run_fourth_example_button = st.button("Run example", key="dp-shortest-clause-prop-fourth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(fourth_example_text, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST,))

	with fifth_example_col:
		fifth_example_text = st.text_area("Example #5", "[[n(a), n(e), b], [n(d), e, n(b)], [n(e), f, n(b)], [f, n(a), e], [e, f, n(b)]].", disabled=True)
		run_fifth_example_button = st.button("Run example", key="dp-shortest-clause-prop-fifth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(fifth_example_text, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST,))

	with sixth_example_col:
		sixth_example_text = st.text_area("Example #6", "[[a, b], [n(a), n(b)], [n(a), b], [a, n(b)]].", disabled=True)
		run_sixth_example_button = st.button("Run example", key="dp-shortest-clause-prop-sixth-example", icon=":material/arrow_forward_ios:", on_click=submit_to_prolog_subprocess, args=(sixth_example_text, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST,))

	st.header("Custom Input")
	custom_example_input = st.text_area("Custom Input", "(a or b) and (~a or ~b) and c", placeholder="For negation of a symbol please use ~.")
	run_custom_input_button = st.button("Run custom input", key="dp-shortest-clause-run-custom-button", icon=":material/arrow_forward_ios:", type="primary", on_click=submit_to_prolog_subprocess, args=(custom_example_input, PrologProcedureEnum.DAVIS_PUTNAM_SHORTEST, True,))

	st.header("SWI-Prolog Output")
	output_text_area = st.text_area("SWI-Prolog Output", st.session_state["prolog_output"], disabled=True, placeholder="Here will be displayed the output of the prolog program.")


st.set_page_config(layout="wide")
pages = {
	"Resolution": [
		st.Page(resolution_fol_streamlit_page, title="Resolution FOL"),
		st.Page(resolution_propositional_streamlit_page, title="Resolution Propositional")
	],
	"Davis Putnam": [
		st.Page(davis_putnam_most_frequent_page, title="Davis Putnam - Most Frequent Strategy"),
		st.Page(davis_putnam_short_clause_page, title="Davis Putnam - Shortest Clause Strategy")
	]
}

streamlit_web_application = st.navigation(pages)
if __name__ == "__main__":
    streamlit_web_application.run()
