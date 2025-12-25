'''
GUIDELINES:
1. Sub templates are prefixed with `st`, `ST`, `St`
'''


from jinja2 import Environment, FileSystemLoader, StrictUndefined

import p_consts


class TranslateAny:
  class System:
    # Jinwoo
    DEFAULT = (
      'You are an expert software engineer who is aware of {src_language} and {tar_language} language features.\n'
      '\n'
      'The ultimate goal of the user is to translate a {src_language} program into a semantically equivalent {tar_language} program.\n'
      'The user decided to translate the source program by using translation rules for each statement.\n'
      'The user currently wants to extract translation rules based on the given source code snippet and semantically equivalent {tar_language} code snippets.\n'
      'However, the user does not have the {tar_language} code snippets.\n'
      'Therefore, your task is to provide semantically equivalent {tar_language} code snippets from the given {src_language} code snippet.\n'
      '\n'
      'Note that one {src_language} code can be translated into multiple semantically equivalent {tar_language} programs, depending on the types of variables in the {src_language} program.\n'
      'For example, the Python code `x in y` can be translated into `y.includes(x);` in JavaScript when `y` is a list in Python, but it can also be translated into `Object.prototype.hasOwnProperty.call(y, x);` in JavaScript when `y` is a dictionary in Python.\n'
      'As you can see in this example case, you should always think of all the possible types of variables which appears in the code and give the user all the possible {tar_language} translations that are semantically equivalent to the given {src_language} code.\n'
      '\n'
      'Consider all the possible types of variables in the {src_language} code and translate the given {src_language} programs to semantically equivalent {tar_language} programs as follows:\n'
      '1. List up all the possible combinations of variable types in the {src_language} code.\n'
      '2. For each case, translate the {src_language} code into a semantically equivalent {tar_language} program.\n'
      '3. The translated {tar_language} program should be surrounded with triple backticks (i.e. \'```\').\n'
      '4. If some features in {src_language} programming language cannot be translated into {tar_language}, just ignore them and focus on semantic equivalence.\n'
    )

    REDUCED = (
      'You are an expert software engineer familiar with {src_language} and {tar_language}.\n'
      'Given a {src_language} code snippet, provide all semantically equivalent {tar_language} translations, considering all meaningful combinations of variable types (choose from: bool, int, str, list, dict, set, user-defined type).\n'
      'Instructions:\n'
      '1. List all meaningful combinations of variable types for the snippet.\n'
      '2. For each case, translate the {src_language} code into a semantically equivalent {tar_language} snippet.\n'
      '3. Output each translation in a separate code block, using triple backticks (e.g., ```).\n'
      '4. Do not include any explanations, comments, or text outside the code blocks.\n'
      '5. If a feature cannot be translated, skip it and focus on semantic equivalence.\n'
      '6. Code blocks must contain only code—no comments or explanations.\n'
      '7. Each {tar_language} translation must be a single statement.\n'
      'Example output:\n'
      '```\n'
      'y.includes(x);\n'
      '```\n'
      '```\n'
      'Object.prototype.hasOwnProperty.call(y, x);\n'
      '```\n'
    )

  class Prompt:
    _prompt = (
      'Translate the following {src_language} snippet into a semantically equivalent {tar_language} snippet(s):\n'
      '```{src_language}\n'
      '{program_to_translate}\n'
      '```\n'
    )

    _prompt_reduced = (
      'Translate the following {src_language} snippet into a semantically equivalent {tar_language} snippet(s):\n'
      '```\n'
      '{program_to_translate}\n'
      '```\n'
    )

    _output_description = (
      'YOUR OUTPUT SHOULD BE AS FOLLOWS:\n'
      '1. **Step-by-Step Explanation**:\n'
      '   Provide a detailed reasoning process for the translation, explaining key decisions and mappings.\n'
      '2. **All possible translated {tar_language} snippets**:\n'
      '   Depending on the types of variables in the snippet, the final {tar_language} translation may look different.\n'
      '   Consider all possible scenarios when it comes to data types of variables in the snippet,\n'
      '   and for each possible data type, provide a proper translation to {tar_language}.\n'
      '3. **Number of statements in {tar_language} snippets**:\n'
      '   Each {tar_language} translation must be a single statement.\n'
      '4. **Output format**\n'
      '   Each {tar_language} translation should be placed in a separate code block surrounded by ```triple backticks```.\n'
      '   ```triple backticks``` must be used for final translations only. Use `single backtick` in all other cases if necessary.\n'
      '   Put explanation or comments outside of ```triple backticks``` code block.\n'
      '5. **Clean code blocks**\n'
      '   Code blocks with {tar_language} translations must contain only code and no comments.\n'
    )

    _output_description_reduced = (
      ''
    )

    _constraints = (
      'CONSTRAINTS:\n'
      '1. When translating assignment expression or assignment statement to JavaScript, provide exactly two translations:\n'
      '   i. Variable declaration with `var` (e.g. `a = 1` -> `var a = 1;`)\n'
      '   ii. Assignment expression without `var` (e.g. `a = 1` -> `a = 1;`)\n'
      '2. When translating `==` operator to JavaScript, provide exactly two translations:\n'
      '   i. Using `==` (e.g. `a == b` -> `a == b`)\n'
      '   ii. Using `===` (e.g. `a == b` -> `a === b`)\n'
      '3. If the {tar_language} translation is a compound statement like `if_statement`, `while_statement`,\n'
      '   or `for_statement`, you must use braces "{{" and "}}" to denote the body of the compound statement.\n'
    )

    _constraints_reduced = (
      'CONSTRAINTS:\n'
      '1. When translating assignment statements to JavaScript, provide exactly two translations:\n'
      '   i. With `var` (`var a = 1;`)\n'
      '   ii. Without `var` (`a = 1;`)\n'
      '2. When translating `==` operator to JavaScript, provide exactly two translations:\n'
      '   i. Using `==` (`a == b`)\n'
      '   ii. Using `===` (`a === b`)\n'
      '3. If the {tar_language} translation is a compound statement like `if_statement`, `while_statement`,\n'
      '   or `for_statement`, you must use braces "{{" and "}}" to denote the body of the compound statement.\n'
    )

    DIRECT_TRANS = (
      f'{_prompt}'
      f'{_output_description}'
      f'{_constraints}'
    )

    DIRECT_TRANS_REDUCED = (
      f'{_prompt_reduced}'
      f'{_output_description_reduced}'
      f'{_constraints_reduced}'
    )

    # seems not helpful enough
    DIRECT_TRANS_WITH_REFERENCE_deprecated = (
      '<<<reference information section>>>\n'
      '\n'
      'The following snippet of {src_language} code is generated by a custom program generator:\n'
      '```{src_language}\n'
      '# generated snippet\n'
      '{program_to_translate}\n'
      '```\n'
      '\n'
      'To generate that snippet of code, the generator used the following snippet of {src_language} code:\n'
      '```{src_language}\n'
      '# original snippet\n'
      '{template_origin}\n'
      '```\n'
      '\n'
      'The original snippet above is taken from the following {src_language} program:\n'
      '```{src_language}\n'
      '# program from which the original snippet is taken\n'
      '{src_program}\n'
      '```\n'
      '\n'
      'The generated snippet of code is similar to the human-written snippet of code.\n'
      'This similarity should be used to infer types of variables in the generated snippet of code\n'
      'by drawing parallels between the generated snippet of code and human-written snippet of code.\n'
      '\n'
      '<<<end of the reference information section>>>\n'
      '\n'
      '<<<task section>>>\n'
      f'{_prompt}'
      f'{_output_description}'
      f'{_constraints}'
      '<<<end of the task section>>>\n'
    )

    # seems not helpful enough
    DIRECT_TRANS_WITH_REFERENCE_SAME_CONTEXT_deprecated = (
      '<<<reference information section>>>\n'
      '\n'
      'The following snippet of {src_language} code is generated by a custom program generator:\n'
      '```{src_language}\n'
      '# generated snippet\n'
      '{program_to_translate}\n'
      '```\n'
      '\n'
      'To generate that snippet of code, the generator used the following snippet of {src_language} code:\n'
      '```{src_language}\n'
      '# original snippet\n'
      '{template_origin}\n'
      '```\n'
      '\n'
      'The generated snippet of code is similar to the human-written snippet of code.\n'
      'This similarity should be used to infer types of variables in the generated snippet of code\n'
      'by drawing parallels between the generated snippet of code and human-written snippet of code.\n'
      '\n'
      '<<<end of the reference information section>>>\n'
      '\n'
      '<<<task section>>>\n'
      f'{_prompt}'
      f'{_output_description}'
      f'{_constraints}'
      '<<<end of the task section>>>\n'
    )

  class Feedback:
    class ParseError:
      CAND_DESC = (
        'The following {tar_language} snippet you provided:\n'
        '```{tar_language}\n'
        '{cand_code}\n'
        '```\n'
        'has a syntax error (according to Tree-sitter parser).\n'
      )

      MAIN = (
        '**PROBLEM WITH THE GENERATED PROGRAM(S)**\n'
        '{cand_descs}\n'
        '**TASK**\n'
        'Please provide translation(s) without syntax errors.\n'
      )

    PARPROG_AFFIX_VIOLATED = (
      'Put the translations into\n'
      '```{tar_language}\n'
      '{partial_program}\n'
      '```\n'
      'by replacing `{variable_to_replace}`.\n'
    )

class TranslateSP1:
  class PartialProgram:
    class Prompt:
      _prompt = (
        'The following snippet of {src_language} code\n'
        '```{src_language}\n'
        '{src_snippet_to_translate}\n'
        '```\n'
        'appears in the following context (in other words, it is a piece of the following larger snippet of {src_language} code)\n'
        '```{src_language}\n'
        '{src_snippet_context}\n'
        '```\n'
        '\n'
        'Your task is to translate this snippet of {src_language} code\n'
        '```{src_language}\n'
        '{src_snippet_to_translate}\n'
        '```\n'
        'into a semantically equivalent snippet of {tar_language} code.\n'
        '\n'
        'Place the translation of\n'
        '```{src_language}\n'
        '{src_snippet_to_translate}\n'
        '```\n'
        'into\n'
        '```{tar_language}\n'
        '{tar_partial_program}\n'
        '```\n'
        'by replacing `{variable_to_replace}` with the translation.\n'
      )

      _prompt_reduced = (
        'The following {src_language} snippet\n'
        '```\n'
        '{src_snippet_to_translate}\n'
        '```\n'
        'appears in the following context (in other words, it is a piece of the following larger {src_language} snippet)\n'
        '```\n'
        '{src_snippet_context}\n'
        '```\n'
        '\n'
        'Your task is to translate this snippet into a semantically equivalent {tar_language} snippet.\n'
        '\n'
        'Place the translation of\n'
        '```\n'
        '{src_snippet_to_translate}\n'
        '```\n'
        'into\n'
        '```\n'
        '{tar_partial_program}\n'
        '```\n'
        'by replacing `{variable_to_replace}` with the translation.\n'
      )

      _output_description = (
        'YOUR OUTPUT SHOULD BE AS FOLLOWS:\n'
        '1. **All possible translated {tar_language} snippets**:\n'
        '   Provide all valid ways to translate `{src_snippet_to_translate}`, and put each translation in a separate code block.\n'
        '   Depending on the types of variables in the snippet, the final {tar_language} translation may look different.\n'
        '   Consider all possible scenarios when it comes to data types of variables in the snippet,\n'
        '   and for each possible data type, provide a proper translation to {tar_language}.\n'
        '2. **Output format**\n'
        '   Each {tar_language} translation should be placed in a separate code block surrounded by ```triple backticks```.\n'
        '   ```triple backticks``` must be used for final translations only. Use `single backtick` in all other cases if necessary.\n'
        '   Put explanation or comments outside of ```triple backticks``` code block.\n'
        '3. **Clean code blocks**\n'
        '   Code blocks with {tar_language} translations must contain only code and no comments.\n'
        '4. **Context preservation**\n'
        '   Everything outside of `{variable_to_replace}` is a context. CONTEXT HAS TO STAY UNCHANGED.\n'
        '   Only `{variable_to_replace}` inside needs to be replaced by the translation . The rest of the code has to remain untouched.\n'
        '   I repeat, only `{variable_to_replace}` needs to be replaced. The rest of the code has to remain untouched.\n'
        '   Do not add or remove any whitespace characters, commas, periods or any other symbols. Replace only `{variable_to_replace}`. You must include the context in your response.\n'
      )

      _output_description_reduced = (
        'YOUR OUTPUT SHOULD BE AS FOLLOWS:\n'
        '1. **Context preservation**\n'
        '   Everything outside of `{variable_to_replace}` is context. CONTEXT HAS TO STAY UNCHANGED.\n'
        '   Only `{variable_to_replace}` inside needs to be replaced by the translation . The rest of the code has to remain untouched.\n'
        '   I repeat, only `{variable_to_replace}` needs to be replaced. The rest of the code has to remain untouched.\n'
        '   Do not add or remove any whitespace characters, commas, periods or any other symbols. Replace only `{variable_to_replace}`. You must include the context in your response.\n'
      )

      _constraints = (
        'CONSTRAINTS:\n'
        '1. When translating `==` operator to JavaScript, provide exactly two translations:\n'
        '   i. Using `==` (e.g. `a == b` -> `a == b`)\n'
        '   ii. Using `===` (e.g. `a == b` -> `a === b`)\n'
      )

      _constraints_reduced = (
        'CONSTRAINTS:\n'
        '1. When translating `==` operator to JavaScript, provide exactly two translations:\n'
        '   i. Using `==` (`a == b`)\n'
        '   ii. Using `===` (`a === b`)\n'
      )

      DEFAULT = (
        f'{_prompt}'
        f'{_output_description}'
        f'{_constraints}'
      )

      REDUCED = (
        f'{_prompt_reduced}'
        f'{_output_description_reduced}'
        f'{_constraints_reduced}'
      )

    class Feedback:
      class MissingContext:
        '''
        **INTRODUCTION**

        The following JavaScript code you generated
        ```JavaScript
        let id_hiw = id_h;
        ```

        (1) was obtained from translating the following Python program
        ```Python
        id_hiw = id_h
        ```

        and (2) has the following AST:
        ```
        program
          lexical_declaration
            variable_declarator
              identifier
              identifier
        ```

        **PROBLEM WITH THE GENERATED PROGRAM**

        This JavaScript code does not fit my requirements.

        I want you to give me a translation such that the root of its AST is something similar to

        ```
        program
          expression_statement
            <the rest of the AST goes here>
        ```
        '''

        class StGrammar_CandsNumber:
          SINGULAR = (
            'This {tar_language} code snippet does not fit my requirements.\n'
            'I want you to give me a translation such that the root of its AST is something similar to\n'
          )
          PLURAL = (
            'These {tar_language} code snippets do not fit my requirements.\n'
            'I want you to give me translations such that the root of their AST is something similar to\n'
          )

        ST_TP1_CAND_DESC = (
          'The following {tar_language} code you generated\n'
          '```{tar_language}\n'
          '{tp1_cand}\n'
          '```\n'
          '(1) was obtained from translating the following {src_language} program\n'
          '```{src_language}\n'
          '{sp1}\n'
          '```\n'
          'and (2) has the following AST:\n'
          '```\n'
          '{tp1_cand_ast_current}\n'
          '```\n'
        )

        MAIN = (
          '**INTRODUCTION**\n'
          '{st_tp1_cand_descs}\n'
          '**PROBLEM WITH THE GENERATED PROGRAM(S)**\n'
          '{st_grammar_cands_number}\n'
          '```\n'
          '{tp1_cand_ast_desired}\n'
          '```\n'
        )

# deprecated since we manually translate SP2 ourselves now
class TranslateSP2_deprecated:
  class Prompt:
    DIRECT_TRANS_SIMILAR = (
      'The following {src_language} program:\n'
      '```{src_language}\n'
      '{sp1}\n'
      '```\n'
      'can be translated into the following semantically equivalent {tar_language} program:\n'
      '```{tar_language}\n'
      '{tp1_cand}\n'
      '```\n'
      '\n'
      'Translate the following {src_language} program:\n'
      '```{src_language}\n'
      '{sp2}\n'
      '```\n'
      'into a semantically equivalent {tar_language} program such that its translation is similar to:\n'
      '```{tar_language}\n'
      '{tp1_cand}\n'
      '```\n'
    )

    PARTIAL_PROGRAM_SIMILAR = (
      '**INTRODUCTION**\n'
      '\n'
      'The following snippet of {src_language} code:\n'
      '```{src_language}\n'
      '{snippet_to_translate_sp2}\n'
      '```\n'
      'appears in the following context (in other words, it is a piece of the following larger snippet of {src_language} code):\n'
      '```{src_language}\n'
      '{snippet_context_sp2}\n'
      '```\n'
      '\n'
      '**TASK**\n'
      '\n'
      'Translate this snippet of {src_language} code\n'
      '```{src_language}\n'
      '{snippet_to_translate_sp2}\n'
      '```\n'
      'into a semantically equivalent snippet of {tar_language} code.\n'
      '\n'
      '**INSTRUCTION 1**\n'
      '\n'
      'Place the translation of\n'
      '```{src_language}\n'
      '{snippet_to_translate_sp2}\n'
      '```\n'
      'into\n'
      '```{tar_language}\n'
      '{partial_program}\n'
      '```\n'
      'by replacing `{variable_to_replace}` with the translation. The resulting {tar_language} program should be syntactically valid.\n'
      '\n'
      '**INSTRUCTION 2**\n'
      '\n'
      'Everything outside of `{variable_to_replace}` is considered to be a context. The context HAS TO REMAIN UNTOUCHED.\n'
      'Only `{variable_to_replace}` needs to be replaced. THE REST OF THE CODE HAS TO REMAIN UNTOUCHED.\n'
      'I repeat, only `{variable_to_replace}` needs to be replaced. THE REST OF THE CODE HAS TO REMAIN UNTOUCHED.\n'
      'Do not add or remove any whitespace characters, commas, periods, semicolons or any other symbols. Replace only `{variable_to_replace}`.\n'
      '\n'
      '**INSTRUCTION 3**\n'
      '\n'
      'The result MUST BE SIMILAR TO\n'
      '```{tar_language}\n'
      '{tp1_cand}\n'
      '```\n'
      '\n'
      'Where\n'
      '```{tar_language}\n'
      '{tp1_cand}\n'
      '```\n'
      'was obtained by translating\n'
      '```{src_language}\n'
      '{sp1}\n'
      '```\n'
      '\n'
      '**INSTRUCTION 4**\n'
      '\n'
      'Provide all valid ways to translate `{snippet_to_translate_sp2}` (if any), and put each translation in a separate code block.\n'
    )

# deprecated since generating test functions is expensive
class GenTestFunction_deprecated:
  '''
  Contains templates for generating test functions for
  validating the translation rules.
  '''
  class System:
    GENERIC_PY = (
      'You are a world class software tester. You specialize in Python programming language.'
    )

  class Context:
    GENERIC_PY = (
      'You will be given a Python function with one or more parameters.\n'
      'Your task is to generate a set of inputs for this functions.\n'
      'You need to use your deep knowledge of Python programming language to correctly infer the types of the parameters.\n'
      '\n'
      'The generated inputs must satisfy the following conditions:\n'
      '1. The inferred types must be correct. (Strive to create inputs with correct types)\n'
      '2. The inputs must cover as many statements as possible. (Strive to cover the code as much as possible)\n'
      '\n'
      'Below, I will explain the format of your response with an example.\n'
      '\n'
      '## Example\n'
      '\n'
      'This is a function for which you need to generate inputs:\n'
      '```py\n'
      'def f_gold(nums, target):\n'
      '''    helper = {{1: 'a', 2: 'b'}}\n'''
      '    for i, v in enumerate(nums):\n'
      '        num = target - v\n'
      '        if num in helper:\n'
      '            return 1\n'
      '    return 0\n'
      '```\n'
      '\n'
      'Here are the possible inputs:\n'
      '1. `f_gold([], 0)` - correctly inferred the type of `nums`, which must be a sequence.\n'
      '2. `f_gold([1], 3)` - covers the body of the for statement and the if statement.\n'
      '3. `f_gold([1], 4)` - covers `then` branch of the if statement inside the for statement.\n'
      '\n'
      'The outputs are then put into a function called `test`:\n'
      '```py\n'
      'def test():\n'
      '    args_sets = [([], 0), ([1], 3), ([1], 4)]\n'
      '    for idx, args_set in enumerate(args_sets):\n'
      '        f_gold(*args_set)\n'
      '```\n'
      '\n'
      'The entire test script will then look as follows:\n'
      '```py\n'
      'def f_gold(nums, target):\n'
      '''    helper = {{1: 'a', 2: 'b'}}\n'''
      '    for i, v in enumerate(nums):\n'
      '        num = target - v\n'
      '        if num in helper:\n'
      '            return 1\n'
      '    return 0\n'
      '\n'
      'def test():\n'
      '    args_sets = [([], 0), ([1], 3), ([1], 4)]\n'
      '    for idx, args_set in enumerate(args_sets):\n'
      '        f_gold(*args_set)\n'
      '\n'
      'test()\n'
      '```\n'
      '\n'
      '## Response format\n'
      '\n'
      'Your response must be a `test()` function where `__generated__arguments__` are the inputs you came up with.\n'
      '```py\n'
      'def test():\n'
      '    args_sets = [__generated__arguments__]\n'
      '    for idx, args_set in enumerate(args_sets):\n'
      '        f_gold(*args_set)\n'
      '```\n'
      '\n'
      '1. **Step-by-Step Explanation**:\n'
      '   Provide a detailed reasoning process for the test generation, explaining key decisions.\n'
      '2. **Output**:\n'
      '   The final `test()` function must be surrounded with ```triple backticks```. For other code snippets, use `single backticks` where necessary.\n'
      '   Use ```triple backticks``` **only** for the generated `test()` function. Do not use triple backticks for any other part of your response.\n'
      '   All other code snippets or explanations should use single backticks (`) where necessary.\n'
      '3. **No comments**:\n'
      '   Replace `__generated__arguments__` with only the inputs you generated. No comments are required explaining the inputs.\n'
      '   I repeat. Do not include comments in the final `test()` function.\n'
      '4. **No need to test different data types**\n'
      '   If you can achieve full coverage with one data type, you do not need to test other data types. Always prefer simpler data types.\n'
      '5. **Assume functions defined**\n'
      '   If `f_gold()` uses some functions, assume that they are already defined. You do not need to define or overwrite them.\n'
      '6. **No list comprehensions**\n'
      '   Do not use list comprehensions in the `test()` function.\n'
      '   Instead, provide the fully expanded list or matrix as a literal, equivalent to the list comprehension.\n'
    )

  class Prompt:
    GENERIC_PY = (
      'Generate a test function for\n'
      '\n'
      '```py\n'
      '{f_gold_function}\n'
      '```\n'
    )

class GetReferenceTranslation:
  class Prompt:
    _prompt = (
      'Translate the following {src_language} statement into a semantically equivalent {tar_language} statement:\n'
      '```{src_language}\n'
      '{statement_to_translate}\n'
      '```\n'
    )

    _prompt_reduced = (
      'Translate the following {src_language} statement into a semantically equivalent {tar_language} statement:\n'
      '```\n'
      '{statement_to_translate}\n'
      '```\n'
    )

    _output_description = (
      'YOUR OUTPUT SHOULD BE AS FOLLOWS:\n'
      '1. **Step-by-Step Explanation**:\n'
      '   Provide a detailed reasoning process for the translation, explaining key decisions and mappings.\n'
      '2. **The translated {tar_language} program**:\n'
      '   The final {tar_language} translation should be syntactically and semantically valid.\n'
      '3. **Output format**\n'
      '   Each {tar_language} translation should be placed in a separate code block surrounded by ```triple backticks```.\n'
      '   ```triple backticks``` must be used for final translations only. Use `single backtick` in all other cases if necessary.\n'
      '   Put explanation or comments outside of ```triple backticks``` code block.\n'
      '4. **Clean code blocks**\n'
      '   Code blocks with {tar_language} translations must contain only code and no comments.\n'
      '   I repeat, code blocks with {tar_language} translations must contain only code and no comments.\n'
    )

    _output_description_reduced = (
      ''
    )

    _constraints = (
      'CONSTRAINTS:\n'
      '1. The {tar_language} translation should be a single statement.\n'
      '   I repeat, the {tar_language} translation should be a single statement.\n'
      '2. When translating assignment expression or assignment statement to JavaScript, provide exactly two translations:\n'
      '   i. Variable declaration with `var` (e.g. `a = 1` -> `var a = 1;`)\n'
      '   ii. Assignment expression without `var` (e.g. `a = 1` -> `a = 1;`)\n'
      '3. When translating `==` operator to JavaScript, provide exactly two translations:\n'
      '   i. Using `==` (e.g. `a == b` -> `a == b`)\n'
      '   ii. Using `===` (e.g. `a == b` -> `a === b`)\n'
      '4. If the {tar_language} translation is a compound statement like `if_statement`, `while_statement`,\n'
      '   or `for_statement`, you must use braces "{{" and "}}" to denote the body of the compound statement.\n'
      '5. The structure of control flow statements (such as if, elif, else, while, for) in the {src_language} \n'
      '   code must be preserved exactly in the {tar_language} translation. Do not merge, remove, \n'
      '   or optimize away any branches, even if their bodies are identical.\n'
      '6. Any function call named secret_fun_4071() that appears as the body of a control flow statement is a \n'
      '   placeholder and must be translated as an equivalent function call in the {tar_language} code, preserving the control flow structure.\n'
      '7. Do not optimize, merge, or remove any code or branches, even if they appear redundant or have identical bodies. \n'
      '   The translation must match the structure of the original code exactly.\n'
    )

    _constraints_reduced = (
      'CONSTRAINTS:\n'
      '1. The {tar_language} translation should be a single statement.\n'
      '   I repeat, the {tar_language} translation should be a single statement.\n'
      '2. When translating assignment expression or assignment statement to JavaScript, provide exactly two translations:\n'
      '   i. Variable declaration with `var` (e.g. `a = 1` -> `var a = 1;`)\n'
      '   ii. Assignment expression without `var` (e.g. `a = 1` -> `a = 1;`)\n'
      '3. When translating `==` operator to JavaScript, provide exactly two translations:\n'
      '   i. Using `==` (e.g. `a == b` -> `a == b`)\n'
      '   ii. Using `===` (e.g. `a == b` -> `a === b`)\n'
      '4. If the {tar_language} translation is a compound statement like `if_statement`, `while_statement`,\n'
      '   or `for_statement`, you must use braces "{{" and "}}" to denote the body of the compound statement.\n'
      '5. The structure of control flow statements (such as if, elif, else, while, for) in the {src_language} \n'
      '   code must be preserved exactly in the {tar_language} translation. Do not merge, remove, \n'
      '   or optimize away any branches, even if their bodies are identical.\n'
      '6. Any function call named secret_fun_4071() that appears as the body of a control flow statement is a \n'
      '   placeholder and must be translated as an equivalent function call in the {tar_language} code, preserving the control flow structure.\n'
      '7. Do not optimize, merge, or remove any code or branches, even if they appear redundant or have identical bodies. \n'
      '   The translation must match the structure of the original code exactly.\n'
    )

    DEFAULT = (
      f'{_prompt}'
      f'{_output_description}'
      f'{_constraints}'
    )

    REDUCED = (
      f'{_prompt_reduced}'
      f'{_output_description_reduced}'
      f'{_constraints_reduced}'
    )


class TemplateManager:
  def __init__(self):
    self.env = Environment(
      loader=FileSystemLoader(p_consts.TEMPLATES_DIR),
      undefined=StrictUndefined,
      trim_blocks=False
    )

  def render(self, template_name: str, **kwargs) -> str:
    template = self.env.get_template(template_name)
    rendered = template.render(**kwargs)
    rendered = '\n'.join(line for line in rendered.splitlines() if line.strip())
    return rendered


# TEST HARNESSES
def _test_system():
  tm = TemplateManager()
  rendered = tm.render(
    'system.j2',
    use_reduced_prompts=True,
    src_language='Python',
    tar_language='JavaScript'
  )
  print('--- Using reduced prompts ---')
  print(rendered)

  rendered = tm.render(
    'system.j2',
    use_reduced_prompts=False,
    src_language='Python',
    tar_language='JavaScript'
  )
  print('--- Using default prompts ---')
  print(rendered)


def _test_trans_direct():
  tm = TemplateManager()
  rendered = tm.render(
    'trans-sp1-direct.j2',
    use_reduced_prompts=True,
    src_language='Python',
    tar_language='JavaScript',
    program_to_translate='x in y'
  )
  print('--- Using reduced prompts ---')
  print(rendered)

  rendered = tm.render(
    'trans-sp1-direct.j2',
    use_reduced_prompts=False,
    src_language='Python',
    tar_language='JavaScript',
    program_to_translate='x in y'
  )
  print('--- Using default prompts ---')
  print(rendered)


def _test_trans_partial():
  tm = TemplateManager()
  rendered = tm.render(
    'trans-sp1-partial.j2',
    use_reduced_prompts=True,
    src_language='Python',
    tar_language='JavaScript',
    src_snippet_to_translate='x in y',
    variable_to_replace=p_consts.PAR_PROG_PROB_NODE_REPLACE,
    src_snippet_context='''def check_membership(x, y):
    return x in y''',
    tar_partial_program=f'''function check_membership(x, y) return {p_consts.PAR_PROG_PROB_NODE_REPLACE};'''
  )
  print('--- Using reduced prompts ---')
  print(rendered)

  rendered = tm.render(
    'trans-sp1-partial.j2',
    use_reduced_prompts=False,
    src_language='Python',
    tar_language='JavaScript',
    src_snippet_to_translate='x in y',
    variable_to_replace=p_consts.PAR_PROG_PROB_NODE_REPLACE,
    src_snippet_context='''def check_membership(x, y):
    return x in y''',
    tar_partial_program=f'''function check_membership(x, y) return {p_consts.PAR_PROG_PROB_NODE_REPLACE};'''
  )
  print('--- Using default prompts ---')
  print(rendered)


def _test_get_ref_trans():
  tm = TemplateManager()
  rendered = tm.render(
    'get-ref-trans.j2',
    use_reduced_prompts=True,
    src_language='Python',
    tar_language='JavaScript',
    statement_to_translate='x in y'
  )
  print('--- Using reduced prompts ---')
  print(rendered)

  rendered = tm.render(
    'get-ref-trans.j2',
    use_reduced_prompts=False,
    src_language='Python',
    tar_language='JavaScript',
    statement_to_translate='x in y'
  )
  print('--- Using default prompts ---')
  print(rendered)


if __name__ == '__main__':
  _test_system()
  _test_trans_direct()
  _test_trans_partial()
  _test_get_ref_trans()
