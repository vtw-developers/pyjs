# Environment setup
```bash
# conda env
conda create --name pirel_env python>=3.12
conda activate pirel_env

# dependencies
pip install -r requirements.txt

# install NodeJS with NVM https://github.com/nvm-sh/nvm
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
nvm install 21.5.0
```

# Running unit tests for files in `src`
```bash
# from src directory
python -m unittest p_visitor_py_test.py
```


# Understanding the codebase and control flow

## `p_learn_apply_rules`

### Function definitions
1. `cleanup`
2. `learn_phase_on_subject`
3. `learn_and_application_phases_on_subject`
4. `learn_and_application_phases_benchmark_mode`  (entry point 1)
   1. `_load_benchmark_sample`
      1. `_exclude`
   2. `_email_report`
   3. `_load_starting_ruleset`
5. `learn_phase_custom_mode`  (entry point 2)

### Control flow
1. `cleanup`

2. `learn_phase_on_subject`  **MAIN**
   1. **while true**
      1. *p_pirel.*`duoglot_translate_wrapper`
      2. *p_pirel.*`learn_trans_rules_for_prob_node`

3. `learn_and_application_phases_on_subject`
   1. `learn_phase_on_subject`
   2. *p_rule_applicator.*`apply_translation_rules`

4. `learn_and_application_phases_benchmark_mode`  (entry point 1)
   1. `_load_starting_ruleset`
   2. `_load_benchmark_sample`
   3. **foreach subject**
      1. `learn_and_application_phases_on_subject`
      2. `_email_report`
      3. `cleanup`

5. `learn_phase_custom_mode`  (entry point 2)
   1. `learn_phase_on_subject`


## `p_pirel`

### Function definitions
1. `get_partial_program`
   1. `__append_hacky_rules`
   2. `__post_process_partial_program_remove_excess_replace_vars`
2. `learn_trans_rules_from_tsp`
3. `learn_trans_rules_from_tsp_with_retries`
4. `learn_trans_rules_for_prob_node`
   1. `_init_template_dict`
      1. `__rerun_translation_for_context`
      2. `__get_pre_context_global`
      4. `__get_pre_context_local`
   2. `_init_tsps`
5. `duoglot_translate_wrapper`

### Control flow
1. `get_partial_program`
   1. `__append_hacky_rules`
   2. `duoglot_translate_wrapper`
   3. `__post_process_partial_program_remove_excess_replace_vars`
   4. **while true**
      1. `__append_hacky_rules`
      2. `duoglot_translate_wrapper`
      3. `__post_process_partial_program_remove_excess_replace_vars`

2. `learn_trans_rules_from_tsp`
   1. *p_llm_gen.*`get_translation_pairs_from_tsp`
   2. *p_rule_inferencer.*`infer_translation_rules`
   3. *p_rule_validator.*`filter_translation_rules`

3. `learn_trans_rules_from_tsp_with_retries`
   1. **while**
      1. `learn_trans_rules_from_tsp`

4. `learn_trans_rules_for_prob_node`  (invoked from *p_learn_apply_rules*)
   1. `_init_template_dict`
      1. `__rerun_translation_for_context`
      2. *p_grammar.*`simplify_template`
      3. *p_generator.*`simplify_template_with_generator`
      4. `__rerun_translation_for_context`
      5. `get_partial_program`
      6. `__get_pre_context_local`
         1. *p_visitor_py.*`Tree.from_str`
         2. *p_visitor_py.*`PrettyPrinter.visit`
   2. `_init_tsps`
      1. *p_generator.*`generate_tsps_with_generator`
   3. **foreach TSP**
      1. `learn_trans_rules_from_tsp_with_retries`

5. `duoglot_translate_wrapper`
   1. *p_translators.*`get_translator_cached`
   2. *d_grammar_expand.*`TransSession.get_translation`
   3. *d_ast_pretty.*`ast_to_code`


## `p_rule_applicator`

### Function definitions
1. `_postprocess_src_program`
2. `_postprocess_tar_program`
3. `_compare_traces`
4. `_run_tests`
5. `_get_instrumented_src_program`
6. `_get_instrumented_tar_program_plausible`
7. `_get_deinstrumented_tar_program_plausible`
8. `_get_instrumented_tar_test_code`
9. `_get_tar_test_call_code`
10. `_get_tar_main_code`
11. `_concatenate_tar_snippets`
12. `_get_proposed_choices`
    1. `__get_err_line_idx_in_tar_main_code`
    2. `__get_char_pos_to_line_pos_map_lists`
    3. `__find_next_unique_choices`
       1. `___step_choices_list_update`
       2. `___astnode_choices_list_update`
       3. `___choices_any_duplicate`
       4. `___step_choices_list_compare`
       5. `___astnode_choices_list_compare`
13. `apply_translation_rules`  (entry point)

### Control flow
1. `_postprocess_src_program`

2. `_postprocess_tar_program`

3. `_compare_traces`

4. `_run_tests`
   1. *p_code_runner.*`run_src_test_script`
   2. *p_code_runner.*`run_tar_test_script`
   3. `_compare_traces`

5. `_get_instrumented_src_program`
   1. *p_pirel.*`duoglot_translate_wrapper`
   2. `_postprocess_src_program`

6. `_get_instrumented_tar_program_plausible`
   1. `_get_instrumented_tar_test_code`
   2. `_get_tar_test_call_code`
   3. **while true**
      1. `_get_tar_main_code`
      2. `_concatenate_tar_snippets`
      3. `_run_tests`
      4. `_get_proposed_choices`

7. `_get_deinstrumented_tar_program_plausible`
   1. `_get_instrumented_tar_program_plausible`
   2. *p_pirel.*`duoglot_translate_wrapper`
   3. `_postprocess_tar_program`

8. `_get_instrumented_tar_test_code`
   1. *p_pirel.*`duoglot_translate_wrapper`
   2. `_postprocess_tar_program`

9. `_get_tar_test_call_code`

10. `_get_tar_main_code`
    1. *p_pirel.*`duoglot_translate_wrapper`

11. `_concatenate_tar_snippets`

12. `_get_proposed_choices`
    1. `__get_err_line_idx_in_tar_main_code`
    2. `__get_char_pos_to_line_pos_map_lists`
    3. `__find_next_unique_choices`
       1. **one of**
          1. `___step_choices_list_update`
          2. `___astnode_choices_list_update`
       2. `___choices_any_duplicate`
          1. **one of**
             1. `___step_choices_list_compare`
             2. `___astnode_choices_list_compare`

13. `apply_translation_rules`  (entry point)
    1. `_get_instrumented_src_program`
    2. `_get_deinstrumented_tar_program_plausible`
