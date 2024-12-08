from rest_framework import serializers


class AssociationSerializer(serializers.Serializer):
    from_object_type = serializers.ChoiceField(choices=["contacts", "deals"])
    to_object_type = serializers.ChoiceField(choices=["contacts", "deals"])

    """
	associations structure : list of  dictionaries contain one (perform single) or many (perform bulk)
	[ 
          {"from_id": str, "to_id":str },
          {"from_id": str, "to_id":str },
          {"from_id": str, "to_id":str } 
     ]
	"""
    associations = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),  # "from_id" and "to_id" are strings
        )
    )

    def validate(self, data):
        # prevent self-association
        if data["from_object_type"] == data["to_object_type"]:
            raise serializers.ValidationError(
                "Objects cannot be associated with themselves!!")

        return data

    def validate_associations(self, value):
        """
        validate associations field properly to ensure each dict in list contains only 'from_id' and 'to_id' keys and their values are non-empty strings 
        """
        for association in value:
            # required keys
            if not all(key in association for key in ["from_id", "to_id"]):
                raise serializers.ValidationError(
                    "Each association must contain 'from_id' and 'to_id' keys !"
                )

            # non-empty strings
            if not all(isinstance(association[key], str) and association[key].strip() for key in ["from_id", "to_id"]):
                raise serializers.ValidationError(
                    "The 'from_id' and 'to_id' must be non-empty strings !"
                )

            # no extra keys
            extra_keys = set(association.keys()) - {"from_id", "to_id"}
            if extra_keys:
                raise serializers.ValidationError(
                    f"Unexpected keys in association: {', '.join(extra_keys)} !"
                )

        return value
