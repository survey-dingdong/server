from dependency_injector.containers import DeclarativeContainer, WiringConfiguration


class ChatContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=[".adapter.input.api.v1.chat"])
