from email.policy import HTTP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework import status
from hubspot.crm.deals import PublicObjectSearchRequest, Filter, FilterGroup
from hubspot.crm.associations import ApiException
from hubspot.crm.associations.v4 import BatchInputPublicDefaultAssociationMultiPost

from crm_integration.serializers import AssociationSerializer
from .utils import get_hubspot_client


class FetchDealsView(APIView):
    """
       Enable authenticated users to fetch a customized list of deals

    """
    permission_classes = [IsAuthenticated]
    client = get_hubspot_client()

    def get(self, request):
        try:

            response = self.client.crm.deals.basic_api.get_page(
                limit=10, after=request.query_params.get('after'))  # get the first 10 deals

            if response is None or not response.results:
                return Response({"message": "unexpected response received. please try again!"}, status=status.HTTP_400_BAD_REQUEST)

            # parse the deals from the response
            parsed_deals = self.parsed_deals(response.results)

            return Response({"deals": parsed_deals})

        except Exception as e:
            return Response(
                {"message": "An error occurred while fetching deals.", "details": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self):
        # self.client.crm.deals.search_api.do_search()

    def parsed_deals(self, deals):
        parsed_deals = []
        for deal in deals:
            parsed_deals.append({
                "deal_id": deal.id,
                "deal_name": deal.properties.get("dealname", "N/A"),
                "amount": deal.properties.get("amount", "N/A"),
                "deal_stage": deal.properties.get("dealstage", "N/A"),
                "close_date": deal.properties.get("closedate", "N/A"),
                "pipeline": deal.properties.get("pipeline", "N/A"),
                "created_at": deal.properties.get("createdate", "N/A"),
                "deal_link": f"https://app.hubspot.com/deals/{deal.id}"
            }
            )
        return parsed_deals


class FetchContactsView(APIView):
    permission_classes = [IsAuthenticated]
    client = get_hubspot_client()

    def get(self, request):
        try:
            response = self.client.crm.contacts.basic_api.get_page(
                limit=10)

            if response is None or not response.results:
                return Response({"message": "unexpected response received, please try again!"}, status=status.HTTP_400_BAD_REQUEST)

            # parse the contacts from the response
            parsed_contacts = self.parsed_contacts(response.results)

            return Response({"contacts": parsed_contacts})

        except Exception as e:
            return Response(
                {"message": "An error occurred while fetching contacts.",
                    "details": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def parsed_contacts(self, contacts):
        parsed_contacts = []
        for contact in contacts:
            parsed_contacts.append({
                "contact_id": contact.id,
                "contact_name": contact.properties.get("firstname", "N/A") + " " + contact.properties.get("lastname", "N/A"),
                "email": contact.properties.get("email", "N/A"),
                "phone": contact.properties.get("phone", "N/A"),
                "created_at": contact.properties.get("createdate", "N/A"),
                "contact_link": f"https://app.hubspot.com/contacts/{contact.id}"
            })
        return parsed_contacts


class AssociationView(APIView):
    permission_classes = [IsAuthenticated]
    client = get_hubspot_client()

    def post(self, request, *args, **kwargs):
        """
        Create single or batch associations between HubSpot objects [contacts and deals].
        Expects JSON with the following structure :
        {
            "from_object_type": "deals",
            "to_object_type": "contacts",
            "associations": [
                {"from_id": "29909889948", "to_id": "82197844555"},
                {"from_id": "29909889949", "to_id": "82197844556"}  # for bulk
            ]
        }
        """
        serializer = AssociationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)

        # get validated data
        validated_data = serializer.validated_data
        from_object_type = validated_data["from_object_type"]
        to_object_type = validated_data["to_object_type"]
        # List of {"from_id", "to_id"}
        associations = validated_data["associations"]

        # format association list to inputs for the batch API
        inputs = [{"from": {"id": assoc["from_id"]}, "to": {
            "id": assoc["to_id"]}} for assoc in associations]

        # perform association both single and bulk
        try:
            batch_input = BatchInputPublicDefaultAssociationMultiPost(
                inputs=inputs)
            api_response = self.client.crm.associations.v4.batch_api.create_default(
                from_object_type=from_object_type,
                to_object_type=to_object_type,
                batch_input_public_default_association_multi_post=batch_input,
            )
            return Response(api_response.to_dict(), status=status.HTTP_200_OK)

        except ApiException as e:
            return Response({"error": f"HubSpot API error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
