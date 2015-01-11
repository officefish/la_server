#! /usr/bin/env python
# -*- coding: utf-8 -*-



__author__ = 'inozemcev'
from django import forms
from card.models import Card, Race, SubRace
from book.models import Book

CARD_TYPE_CHOISES=[
    ('0','магия'),
    ('1','секрет'),
    ('2','персонаж')
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
    ('27', 'SELF_PLAY')
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
   ('15','INITIATOR_UNIT')
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
    ('18','FREEZE(заморозка)'),
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
    ('37','ACTIVATE(активировать способность)')

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
    'FREEZE(заморозка)',
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
    'ACTIVATE(активировать сособность)'
]

# Вид уникальной способности
EPTITUDE_CONDITION_CHOICES=[
    ('0','NO_CONDITION'),
    ('1','NO_WEAPON'),
    ('2','HAS_WEAPON')
]

EPTITUDE_ATTACHMENT_CHOICES=[
   ('0','ASSOCIATE'),
   ('1','OPPONENT'),
   ('2','ALL')
   ]



class CardForm (forms.Form):

      title = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'maxlength':70}))
      attack = forms.IntegerField(max_value=30, widget=forms.TextInput(attrs={'maxlength':2}))
      health = forms.IntegerField(max_value=30, widget=forms.TextInput(attrs={'maxlength':2}))
      price = forms.IntegerField(max_value=12, widget=forms.TextInput(attrs={'maxlength':2}))
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




class EptitudeForm (forms.Form):

    period = forms.ChoiceField(choices=EPTITUDE_PERIOD_CHOICES)
    level = forms.ChoiceField(choices=EPTITUDE_LEVEL_CHOICES)
    type = forms.ChoiceField(choices=EPTITUDE_TYPE_CHOICES)
    attachment = forms.ChoiceField(choices=EPTITUDE_ATTACHMENT_CHOICES)
    power = forms.IntegerField(max_value=30, initial=0, required=False, widget=forms.TextInput(attrs={'maxlength':2}))
    lifecycle = forms.IntegerField(required=False, initial=0, widget=forms.TextInput(attrs={'maxlength':1}))

    condition = forms.ChoiceField(choices=EPTITUDE_CONDITION_CHOICES)

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

        eptitude_choises = [(-1, '----')]
        eptitude_choises += [ (o.id, etc[o.type]) for o in card.eptitudes]
        self.fields['dependency'] = forms.ChoiceField(required=False, choices=eptitude_choises)

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




