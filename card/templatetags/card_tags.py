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
    '27':'SELF_PLAY'
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
   '15':'INITIATOR_UNIT'
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
	'18':'FREEZE(заморозка)',
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
    '37':'ACTIVATE(активировать способность)'

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
    '2':'HAS_WEAPON'
}


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




