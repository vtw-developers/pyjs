import asyncio
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from pathlib import Path

import p_consts
import p_llm_gen
import p_llm_templates


async def translate(system_message: str, human_message: str) -> str:
  messages = [
    SystemMessage(content=system_message),
    HumanMessage(content=human_message)
  ]
  raw_response, _ = await p_llm_gen.query_llm(messages)
  return raw_response


if __name__ == '__main__':
  dpath = p_consts.ROOT_DIR / Path('test-artifacts/p-visitor-py/function-invocation-replacer')
  for fpath in sorted(dpath.glob('int88888888*in.py')):
    code = fpath.read_text()
    print(f'File: {fpath}')
    print('-' * 80)
    print(code)
    print('-' * 80)

    system_message = p_llm_templates.TranslateAny.System.GENERIC
    human_message = (
      f'Translate the following Python code to JavaScript code. Make sure to use correct JavaScript syntax and semantics.\n'
      f'Do not include any explanations, only provide the translated code:\n'
      f'```\n{code}\n```'
    )

    response = asyncio.run(translate(system_message, human_message))
    print('LLM Response:')
    print(response)
    print('=' * 80)
    print()
