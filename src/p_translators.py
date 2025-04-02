import d_ast_parse
import d_grammar_expand
import d_utils
import p_consts
import p_utils


logger = p_utils.setup_logger(__name__)
_TRANSLATORS_CACHE = {}


def get_translator_cached(
  src_code: str,
  src_lang: str,
  tar_lang: str,
  translation_rules: str,
  slot_dedup_enabled: bool,
) -> d_grammar_expand.TransSession:

  translator_key = d_utils.strings_sha256([src_code, translation_rules, src_lang, tar_lang, str(slot_dedup_enabled)])
  logger.debug(f'get_translator: translator_key={translator_key}, cache size={len(_TRANSLATORS_CACHE)}')

  translator_info = None
  translator = None

  if translator_key in _TRANSLATORS_CACHE:
    logger.debug('Translator found in cache')
    translator_info = _TRANSLATORS_CACHE[translator_key]
    assert translator_info['src_code'] == src_code
    assert translator_info['translation_rules'] == translation_rules
    assert translator_info['src_lang'] == src_lang
    assert translator_info['tar_lang'] == tar_lang
    translator = translator_info['translator']

  else:
    logger.debug('Translator not found in cache')
    src_ast, src_ann = d_ast_parse.parse_text_dbg(src_code, src_lang)
    target_grammar = p_consts.GRAMMAR_DICT[tar_lang]
    _optional_dbg_info_save_func = lambda *args, **kwargs: None

    translator = d_grammar_expand.TransSession(
      src_code,
      src_ast,
      src_ann,
      src_lang,
      tar_lang,
      target_grammar,
      translation_rules,
      _optional_dbg_info_save_func,
      slot_dedup_enabled
    )

    translator_info = {
      'src_code': src_code,
      'src_lang': src_lang,
      'tar_lang': tar_lang,
      'translation_rules': translation_rules,
      'translator': translator
    }
    _TRANSLATORS_CACHE[translator_key] = translator_info

  assert translator is not None and translator_info is not None

  return translator
