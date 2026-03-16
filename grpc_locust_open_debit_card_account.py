from locust import User, between, task

from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_locust_grpc_client
from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class OpenDebitCardAccountScenarioUser(User):
    # Атрибут host обязателен для Locust, даже если он не используется напрямую в gRPC.
    host = "localhost"
    # Время ожидания между задачами от 1 до 3 секунд.
    wait_time = between(1, 3)

    # Аннотации для клиентов и ответов
    users_gateway_client: UsersGatewayGRPCClient
    create_user_response: CreateUserResponse

    accounts_gateway_client: AccountsGatewayGRPCClient
    open_debit_card_account_response: OpenDebitCardAccountResponse

    def on_start(self) -> None:
        """
        Метод, вызываемый при старте каждого виртуального пользователя.
        Здесь происходит инициализация gRPC API клиента и создание пользователя.
        """
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Основная задача виртуального пользователя — открытие дебетового счета.
        Метод будет многократно вызываться Locust-агентами.
        """
        self.users_gateway_client.get_user(self.create_user_response.user.id)
