from rest_framework import serializers
from play.models import Simulation
    
class SimulationSerializer(serializers.Serializer):
    runs = serializers.IntegerField(min_value=1)
    user_hand = serializers.ListField(
        child=serializers.CharField(max_length=3, min_length=2, allow_blank=True),
        min_length=0,
        max_length=2,
        required=False
    )
    
    additional_players = serializers.IntegerField(max_value=7, min_value=1)
    
    additional_hands = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(max_length=3, min_length=2, allow_blank=True),
            min_length=0, 
            max_length=1000),
        required=False
    )
    
    results = serializers.DictField(
        child=serializers.DictField(
            child=serializers.IntegerField(min_value=0)
        ),
        read_only=True
    )
    
    wins = serializers.IntegerField(min_value=0, read_only=True)
    ties = serializers.IntegerField(min_value=0, read_only=True)
    losses = serializers.IntegerField(min_value=0, read_only=True)
    
    def create(self, validated_data):
        return Simulation(**validated_data)
    
    def validate(self, data):
        
        all_starting_hands = []
        if data.get('user_hand'):
            all_starting_hands = data['user_hand'].copy()

        if data.get('additional_hands'):
            for hand in data['additional_hands']:
                all_starting_hands += hand
        
        count_list = [card for card in all_starting_hands if all_starting_hands.count(card) > 1 and card]
        
        if count_list:
            duplicates = ' '.join(list(set(count_list)))
            raise serializers.ValidationError("Cannot submit same card more than once (" + duplicates + ")")
        
        return data
    