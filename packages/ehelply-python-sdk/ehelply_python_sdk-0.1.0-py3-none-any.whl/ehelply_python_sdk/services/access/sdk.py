from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class AuthModel:
    def __init__(
            self,
            access_sdk=None,
            active_participant_uuid=None,
            entity_identifier=None,
            project_uuid=None,
            access_token=None,
            secret_token=None,
            claims=None,
    ) -> None:
        self.access_sdk = access_sdk
        self.active_participant_uuid = active_participant_uuid
        self.entity_identifier = entity_identifier
        self.project_uuid = project_uuid
        self.access_token = access_token
        self.secret_token = secret_token
        self.claims = claims


class AccessSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/access/partitions/" + self.sdk_configuration.project_identifier

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def search_types(self, name: str) -> Union[GenericHTTPResponse, PageResponse]:
        response: PageResponse = transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/permissions/types",
                params={"name": name}
            ),
            schema=PageResponse
        )

        if is_response_error(response):
            return response

        response.transform_dict(pydantic_type=SearchTypeItem)

        return response

    def create_type(self, partition_type: CreateType) -> Union[GenericHTTPResponse, CreateTypeResponse]:
        """

        # Markdown test
        * This is
        * so very
        * epic

        Parameters
        ----------
        partition_type : CreateType
            Pydantic model which defines the parameters of the type to create

        Returns
        -------

        """
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/permissions/types",
                json={"partition_type": partition_type.dict()}
            ),
            schema=CreateTypeResponse
        )

    def create_node(self, partition_type_uuid: str, node: CreateNode) -> Union[GenericHTTPResponse, CreateNodeResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/permissions/types/" + partition_type_uuid + "/nodes",
                json={"node": node.dict()}
            ),
            schema=CreateNodeResponse
        )

    def create_group(self, group: CreateGroup) -> Union[GenericHTTPResponse, CreateGroupResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/who/groups",
                json={"group": group.dict()}
            ),
            schema=CreateGroupResponse
        )

    def create_role(self, role: CreateRole) -> Union[GenericHTTPResponse, CreateRoleResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/roles",
                json={"role": role.dict()}
            ),
            schema=CreateRoleResponse
        )

    def add_entity_to_group(self, entity_identifier: str, group_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/who/groups/" + group_uuid + "/entities/" + entity_identifier
            ),
            schema=MessageResponse
        )

    def attach_key_to_entity(
            self,
            entity_identifier: str,
            key_uuid: str
    ) -> Union[GenericHTTPResponse, AttachKeyToEntityResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/who/entities/" + entity_identifier + "/keys/" + key_uuid
            ),
            schema=AttachKeyToEntityResponse
        )

    def make_rgt(
            self,
            role_uuid: str,
            group_uuid: str,
            target_identifier: str
    ) -> Union[GenericHTTPResponse, MakeRGTResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/rgts/roles/" + role_uuid + "/groups/" + group_uuid + "/targets/" + target_identifier
            ),
            schema=MakeRGTResponse
        )

    def automate_role_group_rgt(
            self,
            role: CreateRole,
            group: CreateGroup,
            target_identifier: str,
            entity_identifiers: List[str] = None
    ) -> Union[GenericHTTPResponse, MakeRGTResponse]:

        role_response: CreateRoleResponse = self.create_role(role=role)

        if is_response_error(role_response):
            return role_response

        group_response: CreateGroupResponse = self.create_group(group=group)

        if is_response_error(group_response):
            return group_response

        if len(entity_identifiers) > 0 and not group.default:
            for entity_identifier in entity_identifiers:
                self.add_entity_to_group(entity_identifier=entity_identifier, group_uuid=group_response.uuid)

        return self.make_rgt(
            role_uuid=role_response.uuid,
            group_uuid=group_response.uuid,
            target_identifier=target_identifier
        )

    def is_entity_allowed(
            self,
            entity_identifier: str,
            target_identifier: str,
            node: str
    ) -> bool:

        response: Response = self.requests_session.get(
            self.get_base_url() + "/auth/targets/" + target_identifier + "/nodes/" + node + "/entities/" + entity_identifier
        )

        if not is_response_error(response) and response.json() is True:
            return True

        # return transform_response_to_schema(response, None)
        return False

    def is_key_allowed(
            self,
            access_token: str,
            secret_token: str,
            target_identifier: str,
            node: str
    ) -> bool:

        headers: dict = {
            "X-Access-Token": access_token,
            "X-Secret-Token": secret_token
        }

        response: Response = self.requests_session.get(
            self.get_base_url() + "/auth/targets/" + target_identifier + "/nodes/" + node + "/keys",
            headers=headers
        )

        if not is_response_error(response) and response.json() is True:
            return True

        # return transform_response_to_schema(response, None)
        return False

    def is_allowed(
            self,
            auth_model: AuthModel,
            target_identifier: str,
            node: str
    ) -> bool:
        if auth_model.entity_identifier:
            if self.is_entity_allowed(
                    entity_identifier=auth_model.entity_identifier,
                    target_identifier=target_identifier,
                    node=node
            ):
                return True

        if auth_model.access_token and auth_model.secret_token:
            if self.is_key_allowed(
                    access_token=auth_model.access_token,
                    secret_token=auth_model.secret_token,
                    target_identifier=target_identifier,
                    node=node
            ):
                return True

        return False
