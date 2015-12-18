#! /usr/bin/env python
# -*- coding: utf-8 -*-



__author__ = 'inozemcev'
from django import forms
from card.models import Card, Race, SubRace
from book.models import Book
from group.models import Group
from weapon.models import Weapon

CARD_TYPE_CHOISES=[
    ('0','магия'),
    ('1','секрет'),
    ('2','персонаж'),
    ('3','магия по цели')
]

# Момент использования уникальной способности
EPTITUDE_PERIOD_CHOICES=[
    ('-1','ACTIVATED'),
    ('0','START_STEP'),
    ('1','END_STEP'),
    ('2','SELF_PLACED'),
    ('3','ASSOCIATE_PLACED'),
    ('4','OPPONENT_PLACED'),
    ('5','ALL_PLACED'),
    ('6','ASSOCIATE_RACE_PLACED'),
    ('7','OPPONENT_RACE_PLACED'),
    ('8','ALL_RACE_PLACED'),
    ('9','SELF_WOUND'),
    ('10','ASSOCIATE_WOUND'),
    ('11','OPPONENT_WOUND'),
    ('12','ALL_WOUND'),
    ('13','SELF_DIE'),
    ('14','ASSOCIATE_DIE'),
    ('15','OPPONENT_DIE'),
    ('16','ALL_DIE'),
    ('17','ASSOCIATE_TREATED'),
    ('18','OPPONENT_TREATED'),
    ('19','ALL_TREATED'),
    ('20','ASSOCIATE_SPELL'),
    ('21','OPPONENT_SPELL'),
    ('22','ALL_SPELL'),
    ('23','ASSOCIATE_PLAY_CARD'),
    ('24','OPPONENT_PLAY_CARD'),
    ('25','ALL_PLAY_CARD'),
    ('26','ATTACK'),
    ('27', 'SELF_PLAY'),
    ('28', 'SELF_FULL_HEALTH'),
    ('29', 'ASSOCIATE_HERO_TREATED'),
    ('30', 'OPPONENT_HERO_TREATED'),
    ('31', 'ALL_HEROES_TREATED'),
    ('32','NEW_CARD_IN_HAND'),
    ('33','NEW_PLAYER_CARD_IN_HAND'),
    ('34','NEW_OPPONENT_CARD_IN_HAND'),
    ('35','CARD_MODE_NEW_UNIT'),
    ('36','CARD_MODE_PLAY_CARD'),
    ('37','CARD_MODE_PLAYER_PLAY_CARD'),
    ('38','CARD_MODE_OPPONENT_PLAY_CARD'),
    ('39','CARD_MODE_UNIT_DIE'),
    ('40','CARD_MODE_PLAYER_HERO_WOUND'),
    ('41','CARD_MODE_NEW_CARD'),
    ('42','CARD_MODE_OPPONENT_HERO_WOUND'),
    ('43','CARD_MODE_DESTROY_SHIELD'),
    ('44','CARD_MODE_FREEZE'),
    ('45','IS_ATTACKED'),
    ('46','OPPONENT_END_STEP'),
    ('47','OPPONENT_START_STEP'),
    ('48','ASSOCIATE_ENTICE'),
    ('49','OPPONENT_ENTICE'),
    ('50','PRE_ATTACK'),
    ('51','OPPONENT_PRE_ATTACK'),
    ('52','ACTIVATE_SPELL_TO_TARGET'),
    ('53','ACTIVATE_SPELL'),
    ('54','ACTIVATE_ACHIEVE'),
    ('55','ACTIVATE_ACTIVE')


]


     # Уровень применения уникальной способности
EPTITUDE_LEVEL_CHOICES=[
   ('0','SELF(к самому себе)'),
   ('1','ALL'),
   ('2','RANDOM'),
   ('3','SELECTED'),
   ('4','LEFT_NEIGHBOR'),
   ('5','RIGHT_NEIGHBOR'),
   ('6','NEIGHBORS'),
   ('7','HERO'),
   ('8','DECK'),
   ('9','HAND'),
   ('10','UNIT_CARDS'),
   ('11','SPELL_CARDS'),
   ('12','LAST_ATTACKED'),
   ('13','LAST_ATTACKED_UNIT'),
   ('14','INITIATOR'),
   ('15','INITIATOR_UNIT'),
   ('16','LAST_PLACED'),
   ('17','ALL_CARDS_IN_HAND'),
   ('18','RANDOM_CARD_IN_HAND'),
   ('19','LAST_CARD_IN_HAND'),
   ('20','LAST_PLAYER_CARD_IN_HAND'),
   ('21','LAST_OPPONENT_CARD_IN_HAND'),
   ('22','LAST_ATTACKING_UNIT'),
   ('23', 'ACTIVE_PLAYER'),
   ('24','SPELL_TARGET'),
   ('25','SPELL_TARGET_ALLIES'),
   ('26','SPELL_TARGET_NEIGHBORS'),
   ('27','ALL_EXCEPT_ONE'),
   ('28','UNIT_HERO'),
   ('29','ACTIVE_TARGET')
]


     # Вид уникальной способности
EPTITUDE_TYPE_CHOICES=[
    ('0','DEPENDENСY(зависимость) тех.'),
    ('1','JERK(рывок)'),
    ('2','DOUBLE_ATTACK(двойная аттака)'),
    ('3','PASSIVE_ATTACK(пассивная аттака)'),
    ('4','PROVOCATION(провокация)'),
    ('5','INCREASE_ATTACK(увеличение аттаки)'),
    ('6','INCREASE_HEALTH(увеличение здоровья)'),
    ('7','DECREASE_ATTACK(уменьшение аттаки)'),
    ('8','DECREASE_HEALTH(уменьшение здоровья)'),
    ('9','CHANGE_ATTACK_TILL(изменение аттаки до)'),
    ('10','CHANGE_HEALTH_TILL(изменение здоровья до)'),
    ('11','FULL_HEALTH(полное восстановление здоровья)'),
    ('12','DUMBNESS(немота)'),
    ('13','TREATMENT(лечение)'),
    ('14','PICK_CARD(карта из колоды)'),
    ('15','BACK_CARD_TO_HAND(возвращение карты в колоду)'),
    ('16','KILL(убийство)'),
    ('17','SHADOW(тень)'),
    ('18','FREEZE_ATTACK(замораживающая аттака)'),
    ('19','NEW_UNIT(новый юнит)'),
    ('20','SHIELD(божественный щит)'),
    ('21','INCREASE_ATTACK_MIXIN(доп.увеличение к аттаке)'),
    ('22','DECREASE_ATTACK_MIXIN(допюцвеличение к здоровью)'),
    ('23','CAN_NOT_ATTACK(не может аттаковать)'),
    ('24','REPLACE_ATTACK_HEALTH(меняет местами аттаку и здоровье)'),
    ('25','SALE(скидка на карту)'),
    ('26','INCREASE_SPELL(увеличение силы магии)'),
    ('27','DECREASE_SPELL(умеьшение силы магии)'),
    ('28','SPELL_INVISIBLE(не доступен для аттак магией)'),
    ('29','MASSIVE_ATTACK(массовая аттака)'),
    ('30','INCREASE_ATTACK_AND_HEALTH(увеличение аттаки и здоровья)'),
    ('31','INCREASE_HEALTH_MIXIN(доп.увеличение к здоровью)'),
    ('32','DECREASE_HEALTH_MIXIN(доп.уменьщение к здоровью)'),
    ('33','ENTICE_UNIT(переманивание юнита)'),
    ('34','NEW_SPELL(новая карта магии)'),
    ('35','COPY_UNIT(копирование юнита)'),
    ('36','UNIT_CONVERTION(превращение юнита в другого)'),
    ('37','ACTIVATE(активировать способность)'),
    ('38','DEFAULT_ATTACK(базовая аттака)'),
    ('39','DEFAULT_HEALTH(базовое здоровье)'),
    ('40','INCREASE_ATTACK_AND_HEALTH_DEPENDS_ON_TOKENS'),
    ('41','UNIT_FROM_DECK(существо из колоды)'),
    ('42','INCREASE_CARD_PRICE'),
    ('43','DECREASE_CARD_PRICE'),
    ('44','INCREASE_HEALTH_DEPENDS_ON_ASSOCIATE_CARDS'),
    ('45','INCREASE_HEALTH_DEPENDS_ON_OPPONENT_CARDS'),
    ('46','DECREASE_PRICE_DEPENDS_ON_TOKENS'),
    ('47','DECREASE_PRICE_DEPENDS_ON_PLAYER_CARDS'),
    ('48','DECREASE_PRICE_DEPENDS_ON_OPPONENT_CARDS'),
    ('49','DECREASE_PRICE_DEPENDS_ON_HERO_HEALTH'),
    ('50','INCREASE_CARD_PRICE_MIXIN'),
    ('51','DECREASE_CARD_PRICE_MIXIN'),
    ('52','DECREASE_PRICE_DEPENDS_ON_RACE_TOKENS'),
    ('53','DECREASE_PRICE_DEPENDS_ON_SHIELD_TOKENS'),
    ('54','DECREASE_PRICE_DEPENDS_ON_DIE_UNITS'),
    ('55','DECREASE_PRICE_DEPENDS_ON_FROZEN_TOKENS'),
    ('56','DECREASE_PRICE_DEPENDS_ON_PLAYER_SPELLS'),
    ('57','DECREASE_PRICE_DEPENDS_ON_OPPONENT_SPELLS'),
    ('58','REPLACE_CARD_AND_TOKEN'),
    ('59',' FREEZE'),
    ('60','SHIELD_PROVOCATION_OR_DOUBLE_ATTACK'),
    ('61','PICK_CARD_TILL'),
    ('62','CHANGE_EXTRA_ATTACK_TILL'),
    ('63','CHANGE_UNIT_TO_RANDOM_FOR_SAME_PRICE'),
    ('64','ATTACK_RANDOM_UNIT'),
    ('65','PRIMARY_TARGET'),
    ('66','INCREASE_MANA'),
    ('67','DECREASE_MANA'),
    ('68','PASSIVE_ATTACK_SERIES'),
    ('69','PASSIVE_ATTACK_FOR_SEVERAL_TARGETS'),
    ('70','ATTACK_EQUAL_TO_HEALTH'),
    ('71','ATTACH_EPTITUDE'),
    ('72','OVERLOAD'),
    ('73','COPY_CARD_FROM_HAND'),
    ('74','DROP_CARD'),
    ('75','SELECT_EFFECT'),
    ('76','SELECT_GUISE'),
    ('77','DESTROY_SHADOW'),
    ('78','MULTIPLY_HEALTH'),
    ('79','GENERATE_UNIT_CARD'),
    ('80','GENERATE_SPELL_CARD'),
    ('81','REBIRTH'),
    ('82','PICK_CARD_DEPENDS_ON_WOUND_UNITS'),
    ('83','COPY_CARD_FROM_DECK'),
    ('84','PICK_CARDS_DEPENDS_ON_OPPONENT_CARDS_COUNT'),
    ('85','UNIT_COPY_FROM_DECK'),
    ('86','UNIT_FROM_HAND'),
    ('87','MASSIVE_ATTACK_DEPENDS_ON_UNIT_ATTACK_VALUE'),
    ('88','MASSIVE_KILL'),
    ('89','MULTIPLY_ATTACK'),
    ('90','MASSIVE_ATTACK_DEPENDS_ON_TARGET_ATTACK_VALUE'),
    ('91','SHUFFLE_UNIT_TO_DECK'),
    ('92','SHUFFLE_UNIT_CARD_TO_DECK'),
    ('93','BACK_SEVERAL_TOKENS_TO_HAND'),
    ('94','COPY_UNIT_CARDS_TO_HAND'),
    ('95','FLY'),
    ('96','DESTROY_PROVOCATION'),
    ('97','TAKE_UP_WEAPON'),
    ('98','CARD_FROM_GRAVEYARD'),
    ('99','MINION_FROM_GRAVEYEARD'),
]

etc = [
    'DEPENDENСY(зависимость) тех.',
    'JERK(рывок)',
    'DOUBLE_ATTACK(двойная аттака)',
    'PASSIVE_ATTACK(пассивная аттака)',
    'PROVOCATION(провокация)',
    'INCREASE_ATTACK(увеличение аттаки)',
    'INCREASE_HEALTH(увеличение здоровья)',
    'DECREASE_ATTACK(уменьшение аттаки)',
    'DECREASE_HEALTH(уменьшение здоровья)',
    'CHANGE_ATTACK_TILL(изменение аттаки до)',
    'CHANGE_HEALTH_TILL(изменение здоровья до)',
    'FULL_HEALTH(полное восстановление здоровья)',
    'DUMBNESS(немота)',
    'TREATMENT(лечение)',
    'PICK_CARD(карта из колоды)',
    'BACK_CARD_TO_HAND(возвращение карты в колоду)',
    'KILL(убийство)',
    'SHADOW(тень)',
    'FREEZE_ATTACK(замораживающая аттака)',
    'NEW_UNIT(новый юнит)',
    'SHIELD(божественный щит)',
    'INCREASE_ATTACK_MIXIN(доп.увеличение к аттаке)',
    'DECREASE_ATTACK_MIXIN(допюцвеличение к здоровью)',
    'CAN_NOT_ATTACK(не может аттаковать)',
    'REPLACE_ATTACK_HEALTH(меняет местами аттаку и здоровье)',
    'SALE(скидка на карту)',
    'INCREASE_SPELL(увеличение силы магии)',
    'DECREASE_SPELL(умеьшение силы магии)',
    'SPELL_INVISIBLE(не доступен для аттак магией)',
    'MASSIVE_ATTACK(массовая аттака)',
    'INCREASE_ATTACK_AND_HEALTH(увеличение аттаки и здоровья)',
    'INCREASE_HEALTH_MIXIN(доп.увеличение к здоровью)',
    'DECREASE_HEALTH_MIXIN(доп.уменьщение к здоровью)',
    'ENTICE_UNIT(переманивание юнита)',
    'NEW_SPELL(новая карта магии)',
    'COPY_UNIT(копирование юнита)',
    'UNIT_CONVERTION(превращение юнита в другого)',
    'ACTIVATE(активировать сособность)',
    'DEFAULT_ATTACK(базовая аттака)',
    'DEFAULT_HEALTH(базовое здоровье)',
    'INCREASE_ATTACK_AND_HEALTH_DEPENDS_ON_TOKENS',
    'UNIT_FROM_DECK(существо из колоды)',
    'INCREASE_CARD_PRICE',
    'DECREASE_CARD_PRICE',
    'INCREASE_HEALTH_DEPENDS_ON_ASSOCIATE_CARDS',
    'INCREASE_HEALTH_DEPENDS_ON_OPPONENT_CARDS',
    'DECREASE_PRICE_DEPENDS_ON_TOKENS',
    'DECREASE_PRICE_DEPENDS_ON_PLAYER_CARDS',
    'DECREASE_PRICE_DEPENDS_ON_OPPONENT_CARDS',
    'DECREASE_PRICE_DEPENDS_ON_HERO_HEALTH',
    'INCREASE_CARD_PRICE_MIXIN',
    'DECREASE_CARD_PRICE_MIXIN',
    'DECREASE_PRICE_DEPENDS_ON_RACE_TOKENS',
    'DECREASE_PRICE_DEPENDS_ON_SHIELD_TOKENS',
    'DECREASE_PRICE_DEPENDS_ON_DIE_UNITS',
    'DECREASE_PRICE_DEPENDS_ON_FROZEN_TOKENS',
    'DECREASE_PRICE_DEPENDS_ON_PLAYER_SPELLS',
    'DECREASE_PRICE_DEPENDS_ON_OPPONENT_SPELLS',
    'REPLACE_CARD_AND_TOKEN',
    'FREEZE',
    'SHIELD_PROVOCATION_OR_DOUBLE_ATTACK',
    'PICK_CARD_TILL',
    'CHANGE_EXTRA_ATTACK_TILL',
    'CHANGE_UNIT_TO_RANDOM_FOR_SAME_PRICE',
    'ATTACK_RANDOM_UNIT',
    'PRIMARY_TARGET',
    'INCREASE_MANA',
    'DECREASE_MANA',
    'PASSIVE_ATTACK_SERIES',
    'PASSIVE_ATTACK_FOR_SEVERAL_TARGETS',
    'ATTACK_EQUAL_TO_HEALTH',
    'ATTACH_EPTITUDE',
    'OVERLOAD',
    'COPY_CARD_FROM_HAND',
    'DROP_CARD',
    'SELECT_EFFECT',
    'SELECT_GUISE',
    'DESTROY_SHADOW',
    'MULTIPLY_HEALTH',
    'GENERATE_UNIT_CARD',
    'GENERATE_SPELL_CARD',
    'REBIRTH',
    'PICK_CARD_DEPENDS_ON_WOUND_UNITS',
    'COPY_CARD_FROM_DECK',
    "PICK_CARDS_DEPENDS_ON_OPPONENT_CARDS_COUNT",
    'UNIT_COPY_FROM_DECK',
    'UNIT_FROM_HAND',
    'MASSIVE_ATTACK_DEPENDS_ON_UNIT_ATTACK_VALUE',
    'MASSIVE_KILL',
    'MULTIPLY_ATTACK',
    'MASSIVE_ATTACK_DEPENDS_ON_TARGET_ATTACK_VALUE',
    'SHUFFLE_UNIT_TO_DECK',
    'SHUFFLE_UNIT_CARD_TO_DECK',
    'BACK_SEVERAL_TOKENS_TO_HAND',
    'COPY_UNIT_CARDS_TO_HAND',
    'FLY (полет)',
    'DESTROY_PROVOCATION',
    'TAKE_UP_WEAPON',
    'CARD_FROM_GRAVEYARD',
    'MINION_FROM_GRAVEYEARD(призыв на стол существ ранее погибших в этом бою)',
]

# Вид уникальной способности
EPTITUDE_CONDITION_CHOICES=[
    ('0','NO_CONDITION'),
    ('1','NO_WEAPON'),
    ('2','HAS_WEAPON'),
    ('3','HAS_SELF_DIE_EPTITUDE'),
    ('4','LAST_PLACED_HAS_SELF_DIE_EPTITUDE'),
    ('5','ATTACK_MORE_THAN_6'),
    ('6','ATTACK_LESS_THAN_3'),
    ('7','HAS_BATTLECRY_EPTITUDE'),
    ('8','ASSOCIATE_CONTROL_MEHANIZM_UNITS'),
    ('9','ASSOCIATE_NO_CONTROL_MEHANIZM_UNITS'),
    ('10','OPPONENT_ROW_LENGTH_MORE_THAN_3'),
    ('11','ATTACK_EQUALS_TO_1'),
    ('12','FULL_HEALTH'),
    ('13','NOT_FULL_HEALTH'),
    ('14','FREEZE'),
    ('15','SPELL_TARGET_DEAD'),
    ('16','SPELL_TARGET_NOT_FULL_HEALTH'),
    ('17','DRAWING_SERIES'),
    ('18','NOT_DRAWING_SERIES'),
    ('19','ATTACHED_EPTITUDE'),
    ('20','ATTACK_LESS_THAN_4'),
    ('21','ANIMAL_CARD'),
    ('22','UNIT_IN_SHADOW'),
    ('23','FULL_MANA'),
    ('24','DEMON_UNIT'),
    ('25','NOT_DEMON_UNIT'),
    ('26','ATTACK_MORE_THAN_4')
]

EPTITUDE_ATTACHMENT_CHOICES=[
   ('0','ASSOCIATE'),
   ('1','OPPONENT'),
   ('2','ALL')
   ]

EPTITUDE_WIDGET=[
   ('0','NO_WIDGET'),
   ('1','DIE_WIDGET'),
   ('2','WOUND_WIDGET'),
   ('3','SPELL_WIDGET'),
   ('4','ATTACK_WIDGET')
   ]

EPTITUDE_ANIMATION_CHOICES=[
   ('-1','NO_ANIMATION'),
   ('1','FROSTBOLT')
   ]



class CardForm (forms.Form):

      title = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'maxlength':70}))
      attack = forms.IntegerField(max_value=30, widget=forms.TextInput(attrs={'maxlength':2}))
      health = forms.IntegerField(max_value=30, widget=forms.TextInput(attrs={'maxlength':2}))
      price = forms.IntegerField(max_value=30, widget=forms.TextInput(attrs={'maxlength':2}))
      description = forms.CharField(required=False, max_length=200, widget=forms.Textarea(attrs={'maxlength':200}))
      type = forms.ChoiceField(choices=CARD_TYPE_CHOISES, widget=forms.RadioSelect())
      auxiliary = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )
      has_weapon = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )
      widget = forms.ChoiceField(choices=EPTITUDE_WIDGET)

      def __init__(self, *args, **kwargs):
            super(CardForm, self).__init__(*args, **kwargs)

            race_choises = [(-1, '----')]
            race_choises += [ (o.id, str(o.title)) for o in Race.objects.all()]

            self.fields['race'] = forms.ChoiceField(required=False, choices=race_choises)

            subrace_choises = [(-1, '----')]
            subrace_choises += [ (o.id, str(o.title)) for o in SubRace.objects.all()]

            self.fields['subrace'] = forms.ChoiceField(required=False, choices=subrace_choises)

            book_choises = [(-1, '----')]
            book_choises += [ (o.id, o.title) for o in Book.objects.all()]
            self.fields ['book'] =  forms.ChoiceField(required=False, choices=book_choises)

            group_choises = [(-1, '----')]
            group_choises += [ (o.id, o.title) for o in Group.objects.all()]
            self.fields ['group'] =  forms.ChoiceField(required=False, choices=group_choises)




class EptitudeForm (forms.Form):

    period = forms.ChoiceField(choices=EPTITUDE_PERIOD_CHOICES)
    level = forms.ChoiceField(choices=EPTITUDE_LEVEL_CHOICES)
    type = forms.ChoiceField(choices=EPTITUDE_TYPE_CHOICES)
    attachment = forms.ChoiceField(choices=EPTITUDE_ATTACHMENT_CHOICES)
    power = forms.IntegerField(max_value=30, initial=0, required=False, widget=forms.TextInput(attrs={'maxlength':2}))
    max_power = forms.IntegerField(max_value=30, initial=0, required=False, widget=forms.TextInput(attrs={'maxlength':2}))
    count = forms.IntegerField(max_value = 30, initial=0, required=False, widget=forms.TextInput(attrs={'maxlength':2}))
    lifecycle = forms.IntegerField(required=False, initial=0, widget=forms.TextInput(attrs={'maxlength':1}))
    probability = forms.IntegerField(min_value=0, max_value=100, initial=100, widget=forms.TextInput(attrs={'maxlength':3}))

    condition = forms.ChoiceField(choices=EPTITUDE_CONDITION_CHOICES)
    spellCondition = forms.ChoiceField(choices=EPTITUDE_CONDITION_CHOICES)


    battlecry = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    spellSensibility = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    dynamic = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    attach_hero = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    attach_initiator = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    activate_widget = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    widget = forms.ChoiceField(choices=EPTITUDE_WIDGET)
    destroy = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )

    manacost = forms.IntegerField(min_value=0, max_value=10, initial=0, widget=forms.TextInput(attrs={'maxlength':2}))
    animation = forms.ChoiceField(choices=EPTITUDE_ANIMATION_CHOICES)



    def __init__(self, card, *args, **kwargs):
        super(EptitudeForm, self).__init__(*args, **kwargs)

        race_choises = [(-1, '----')]
        race_choises += [ (o.id, str(o.title)) for o in Race.objects.all()]
        self.fields['race'] = forms.ChoiceField(required=False, choices=race_choises)

        subrace_choises = [(-1, '----')]
        subrace_choises += [ (o.id, str(o.title)) for o in SubRace.objects.all()]
        self.fields['subrace'] = forms.ChoiceField(required=False, choices=subrace_choises)

        unit_choises = [(-1, '----')]
        unit_choises += [ (o.id, o.title) for o in Card.objects.all()]
        self.fields['unit'] = forms.ChoiceField(required=False, choices=unit_choises)

        group_choises = [(-1, '----')]
        group_choises += [ (o.id, o.title) for o in Group.objects.all()]
        self.fields ['group'] =  forms.ChoiceField(required=False, choices=group_choises)

        self.fields['price'] = forms.IntegerField(required=False, initial=-1, widget=forms.TextInput(attrs={'maxlength':2}))

        eptitude_choises = [(-1, '----')]
        eptitude_choises += [ (o.id, etc[o.type]) for o in card.eptitudes]
        self.fields['dependency'] = forms.ChoiceField(required=False, choices=eptitude_choises)
        attach_eptitude_choises = [(-1, '----')]
        attach_eptitude_choises += [ (o.id, etc[o.type]) for o in card.eptitudes]
        self.fields['attach_eptitude'] = forms.ChoiceField(required=False, choices=attach_eptitude_choises)

        weapon_choises = [(-1, '----')]
        weapon_choises += [ (o.id, str(o.title)) for o in Weapon.objects.all()]
        self.fields['weapon'] = forms.ChoiceField(required=False, choices=weapon_choises)


class RaceForm (forms.Form):
     title = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'maxlength':70}))
     description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'maxlength':200}))

class SubRaceForm (forms.Form):
     title = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'maxlength':70}))
     description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'maxlength':200}))

     def __init__(self, *args, **kwargs):
        super(SubRaceForm, self).__init__(*args, **kwargs)

        race_choises = [(-1, '----')]
        race_choises += [ (o.id, str(o.title)) for o in Race.objects.all()]

        self.fields['race'] = forms.ChoiceField(required=False, choices=race_choises)




