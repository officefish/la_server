# -- coding: utf-8 --


from django import template
register = template.Library()

EPTITUDE_PERIOD = {
    '-1':'ACTIVATED',
    '0':'START_STEP',
    '1':'END_STEP',
    '2':'SELF_PLACED',
    '3':'ASSOCIATE_PLACED',
    '4':'OPPONENT_PLACED',
    '5':'ALL_PLACED',
    '6':'ASSOCIATE_RACE_PLACED',
    '7':'OPPONENT_RACE_PLACED',
    '8':'ALL_RACE_PLACED',
    '9':'SELF_WOUND',
    '10':'ASSOCIATE_WOUND',
    '11':'OPPONENT_WOUND',
    '12':'ALL_WOUND',
    '13':'SELF_DIE',
    '14':'ASSOCIATE_DIE',
    '15':'OPPONENT_DIE',
    '16':'ALL_DIE',
    '17':'ASSOCIATE_TREATED',
    '18':'OPPONENT_TREATED',
    '19':'ALL_TREATED',
    '20':'ASSOCIATE_SPELL',
    '21':'OPPONENT_SPELL',
    '22':'ALL_SPELL',
    '23':'ASSOCIATE_PLAY_CARD',
    '24':'OPPONENT_PLAY_CARD',
    '25':'ALL_PLAY_CARD',
    '26':'ATTACK',
    '27':'SELF_PLAY',
    '28':'SELF_FULL_HEALTH',
    '29':'ASSOCIATE_HERO_TREATED',
    '30':'OPPONENT_HERO_TREATED',
    '31':'ALL_HEROES_TREATED',
    '32':'NEW_CARD_IN_HAND',
    '33':'NEW_PLAYER_CARD_IN_HAND',
    '34':'NEW_OPPONENT_CARD_IN_HAND',
    '35':'CARD_MODE_NEW_UNIT',
    '36':'CARD_MODE_PLAY_CARD',
    '37':'CARD_MODE_PLAYER_PLAY_CARD',
    '38':'CARD_MODE_OPPONENT_PLAY_CARD',
    '39':'CARD_MODE_UNIT_DIE',
    '40':'CARD_MODE_PLAYER_HERO_WOUND',
    '41':'CARD_MODE_NEW_CARD',
    '42':'CARD_MODE_OPPONENT_HERO_WOUND',
    '43':'CARD_MODE_DESTROY_SHIELD',
    '44':'CARD_MODE_FREEZE',
    '45':'IS_ATTACKED',
    '46':'OPPONENT_END_STEP',
    '47':'OPPONENT_START_STEP',
    '48':'ASSOCIATE_ENTICE',
    '49':'OPPONENT_ENTICE',
    '50':'PRE_ATTACK',
    '51':'OPPONENT_PRE_ATTACK',
    '52':"ACTIVATE_SPELL_TO_TARGET",
    '53':'ACTIVATE_SPELL',
    '54':'ACTIVATE_ACHIEVE',
    '55':'ACTIVATE_ACTIVE'

    }

EPTITUDE_LEVEL = {
   '0':'SELF(к самому себе)',
   '1':'ALL',
   '2':'RANDOM',
   '3':'SELECTED',
   '4':'LEFT_NEIGHBOR',
   '5':'RIGHT_NEIGHBOR',
   '6':'NEIGHBORS',
   '7':'HERO',
   '8':'DECK',
   '9':'HAND',
   '10':'UNIT_CARDS',
   '11':'SPELL_CARDS',
   '12':'LAST_ATTACKED',
   '13':'LAST_ATTACKED_UNIT',
   '14':'INITIATOR',
   '15':'INITIATOR_UNIT',
   '16':'LAST_PLACED',
   '17':'ALL_CARDS_IN_HAND',
   '18':'RANDOM_CARD_IN_HAND',
   '19':'LAST_CARD_IN_HAND',
   '20':'LAST_PLAYER_CARD_IN_HAND',
   '21':'LAST_OPPONENT_CARD_IN_HAND',
   '22':'LAST_ATTACKING_UNIT',
   '23':'ACTIVE_PLAYER',
   '24':'SPELL_TARGET',
   '25':'SPELL_TARGET_ALLIES',
   '26':'SPELL_TARGET_NEIGHBORS',
   '27':'ALL_EXCEPT_ONE',
   '28':'UNIT_HERO',
   '29':'ACTIVE_TARGET'
}


     # Вид уникальной способности

EPTITUDE_TYPE = {
    '0':'DEPENDENСY(зависимость) тех.',
    '1':'JERK(рывок)',
    '2':'DOUBLE_ATTACK(двойная аттака)',
    '3':'PASSIVE_ATTACK(пассивная аттака)',
    '4':'PROVOCATION(провокация)',
	'5':'INCREASE_ATTACK(увеличение аттаки)',
	'6':'INCREASE_HEALTH(увеличение здоровья)',
	'7':'DECREASE_ATTACK(уменьшение аттаки)',
	'8':'DECREASE_HEALTH(уменьшение здоровья)',
	'9':'CHANGE_ATTACK_TILL(изменение аттаки до)',
	'10':'CHANGE_HEALTH_TILL(изменение здоровья до)',
	'11':'FULL_HEALTH(полное восстановление здоровья)',
	'12':'DUMBNESS(немота)',
	'13':'TREATMENT(лечение)',
	'14':'PICK_CARD(карта из колоды)',
	'15':'BACK_CARD_TO_HAND(возвращение карты в колоду)',
	'16':'KILL(убийство)',
	'17':'SHADOW(тень)',
	'18':'FREEZE_ATTACK(замораживающая аттака)',
    '19':'NEW_UNIT(новый юнит)',
    '20':'SHIELD(божественный щит)',
    '21':'INCREASE_ATTACK_MIXIN(доп.увеличение к аттаке)',
    '22':'DECREASE_ATTACK_MIXIN(допюцвеличение к здоровью)',
    '23':'CAN_NOT_ATTACK(не может аттаковать)',
    '24':'REPLACE_ATTACK_HEALTH(меняет местами аттаку и здоровье)',
    '25':'SALE(скидка на карту)',
    '26':'INCREASE_SPELL(увеличение силы магии)',
    '27':'DECREASE_SPELL(умеьшение силы магии)',
    '28':'SPELL_INVISIBLE(не доступен для аттак магией)',
    '29':'MASSIVE_ATTACK(массовая аттака)',
    '30':'INCREASE_ATTACK_AND_HEALTH(увеличение аттаки и здоровья)',
    '31':'INCREASE_HEALTH_MIXIN(доп.увеличение к здоровью)',
    '32':'DECREASE_HEALTH_MIXIN(доп.уменьщение к здоровью)',
    '33':'ENTICE_UNIT(переманивание юнита)',
    '34':'NEW_SPELL(новая карта магии)',
    '35':'COPY_UNIT(копирование юнита)',
    '36':'UNIT_CONVERTION(превращение юнита в другого)',
    '37':'ACTIVATE(активировать способность)',
    '38':'DEFAULT_ATTACK(базовая аттака)',
    '39':'DEFAULT_HEALTH(базовое здоровье)',
    '40':'INCREASE_ATTACK_AND_HEALTH_DEPENDS_ON_TOKENS(ув.аттаку и здоровье в зависимости от токенов на поле)',
    '41':'UNIT_FROM_DECK(существо из колоды)',
    '42':'INCREASE_CARD_PRICE',
    '43':'DECREASE_CARD_PRICE',
    '44':'INCREASE_HEALTH_DEPENDS_ON_ASSOCIATE_CARDS',
    '45':'INCREASE_HEALTH_DEPENDS_ON_OPPONENT_CARDS',
    '46':'DECREASE_PRICE_DEPENDS_ON_TOKENS',
    '47':'DECREASE_PRICE_DEPENDS_ON_PLAYER_CARDS',
    '48':'DECREASE_PRICE_DEPENDS_ON_OPPONENT_CARDS',
    '49':'DECREASE_PRICE_DEPENDS_ON_HERO_HEALTH',
    '50':'INCREASE_CARD_PRICE_MIXIN',
    '51':'DECREASE_CARD_PRICE_MIXIN',
    '52':'DECREASE_PRICE_DEPENDS_ON_RACE_TOKENS',
    '53':'DECREASE_PRICE_DEPENDS_ON_SHIELD_TOKENS',
    '54':'DECREASE_PRICE_DEPENDS_ON_DIE_UNITS',
    '55':'DECREASE_PRICE_DEPENDS_ON_FROZEN_TOKENS',
    '56':'DECREASE_PRICE_DEPENDS_ON_PLAYER_SPELLS',
    '57':'DECREASE_PRICE_DEPENDS_ON_OPPONENT_SPELLS',
    '58':'REPLACE_CARD_AND_TOKEN',
    '59':'FREEZE',
    '60':'SHIELD_PROVOCATION_OR_DOUBLE_ATTACK',
    '61':'PICK_CARD_TILL',
    '62':'CHANGE_EXTRA_ATTACK_TILL',
    '63':'CHANGE_UNIT_TO_RANDOM_FOR_SAME_PRICE',
    '64':'ATTACK_RANDOM_UNIT',
    '65':'PRIMARY_TARGET',
    '66':'INCREASE_MANA',
    '67':'DECREASE_MANA',
    '68':'PASSIVE_ATTACK_SERIES',
    '69':'PASSIVE_ATTACK_FOR_SEVERAL_TARGETS',
    '70':'ATTACK_EQUAL_TO_HEALTH',
    '71':'ATTACH_EPTITUDE',
    '72':'OVERLOAD',
    '73':'COPY_CARD_FROM_HAND',
    '74':'DROP_CARD',
    '75':'SELECT_EFFECT',
    '76':'SELECT_GUISE',
    '77':'DESTROY_SHADOW',
    '78':'MULTIPLY_HEALTH',
    '79':'GENERATE_UNIT_CARD',
    '80':'GENERATE_SPELL_CARD',
    '81':'REBIRTH',
    '82':'PICK_CARD_DEPENDS_ON_WOUND_UNITS',
    '83':'COPY_CARD_FROM_DECK',
    '84':'PICK_CARDS_DEPENDS_ON_OPPONENT_CARDS_COUNT',
    '85':'UNIT_COPY_FROM_DECK',
    '86':'UNIT_FROM_HAND',
    '87':'MASSIVE_ATTACK_DEPENDS_ON_UNIT_ATTACK_VALUE',
    '88':'MASSIVE_KILL',
    '89':'MULTIPLY_ATTACK',
    '90':'MASSIVE_ATTACK_DEPENDS_ON_TARGET_ATTACK_VALUE',
    '91':'SHUFFLE_UNIT_TO_DECK',
    '92':'SHUFFLE_UNIT_CARD_TO_DECK',
    '93':'BACK_SEVERAL_TOKENS_TO_HAND',
    '94':'COPY_UNIT_CARDS_TO_HAND',
    '95':'FLY',
    '96':"DESTROY_PROVOCATION",
    '97':"TAKE_UP_WEAPON"
}


EPTITUDE_ATTACHMENT= {
   '0':'ASSOCIATE',
   '1':'OPPONENT',
   '2':'ALL'
}

# Вид уникальной способности
EPTITUDE_CONDITION={
    '0':'NO_CONDITION',
    '1':'NO_WEAPON',
    '2':'HAS_WEAPON',
    '3':'HAS_SELF_DIE_EPTITUDE',
    '4':'LAST_PLACED_HAS_SELF_DIE_EPTITUDE',
    '5':'ATTACK_MORE_THAN_6',
    '6':'ATTACK_LESS_THAN_3',
    '7':'HAS_BATTLECRY_EPTITUDE',
    '8':'ASSOCIATE_CONTROL_MEHANIZM_UNITS',
    '9':'ASSOCIATE_NO_CONTROL_MEHANIZM_UNITS',
    '10':'OPPONENT_ROW_LENGTH_MORE_THAN_3',
    '11':'ATTACK_EQUALS_TO_1',
    '12':'FULL_HEALTH',
    '13':'NOT_FULL_HEALTH',
    '14':'FREEZE',
    '15':'SPELL_TARGET_DEAD',
    '16':'SPELL_TARGET_NOT_FULL_HEALTH',
    '17':'DRAWING_SERIES',
    '18':'NOT_DRAWING_SERIES',
    '19':'ATTACHED_EPTITUDE',
    '20':'ATTACK_LESS_THAN_4',
    '21':'ANIMAL_CARD',
    '22':'UNIT_IN_SHADOW',
    '23':'FULL_MANA',
    '24':'DEMON_UNIT',
    '25':'NOT_DEMON_UNIT',
    '26':'ATTACK_MORE_THAN_4'
}
EPTITUDE_ANIMATION= {
   '-1':'NO_ANIMATION',
   '0':'NO_ANIMATION',
   '1':'FROSTBOLT'
}

@register.filter
def animation(value, arg):
    response = arg

    try:
        response = EPTITUDE_ANIMATION[str(arg)]
    except:
        pass

    return response

@register.filter
def period(value, arg):
    response = arg

    try:
        response = EPTITUDE_PERIOD[str(arg)]
    except:
        pass

    return response

@register.filter
def level(value, arg):
    response = arg

    try:
        response = EPTITUDE_LEVEL[str(arg)]
    except:
        pass

    return response

@register.filter
def type(value, arg):
    response = arg

    try:
        response = EPTITUDE_TYPE[str(arg)]
    except:
        pass

    return response

@register.filter
def attachment(value, arg):
    response = arg

    try:
        response = EPTITUDE_ATTACHMENT[str(arg)]
    except:
        pass

    return response

@register.filter
def bool(value, arg):
    if arg:
        return 'да'
    else:
        return 'нет'

@register.filter
def condition(value, arg):
    response = arg

    try:
        response = EPTITUDE_CONDITION[str(arg)]
    except:
        pass

    return response




