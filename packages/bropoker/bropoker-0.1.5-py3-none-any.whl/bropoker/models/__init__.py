from bropoker.models.registration import register, load

register(
    model_id = 'leduc-holdem-nfsp-pytorch',
    entry_point='bropoker.models.pretrained_models:LeducHoldemNFSPPytorchModel')

register(
    model_id = 'leduc-holdem-cfr',
    entry_point='bropoker.models.pretrained_models:LeducHoldemCFRModel')

register(
    model_id = 'leduc-holdem-rule-v1',
    entry_point='bropoker.models.leducholdem_rule_models:LeducHoldemRuleModelV1')

register(
    model_id = 'leduc-holdem-rule-v2',
    entry_point='bropoker.models.leducholdem_rule_models:LeducHoldemRuleModelV2')

register(
    model_id = 'limit-holdem-rule-v1',
    entry_point='bropoker.models.limitholdem_rule_models:LimitholdemRuleModelV1')
