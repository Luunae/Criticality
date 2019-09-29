from reactor import Reactor


def test_reactor():
    reactor = Reactor()

    step = 0
    while 0 < reactor.status_percentage() < 1:
        print(f"step {step:04d}")
        print("\n".join(reactor.get_statuses()))
        reactor.auto_changes()
        step += 1

    print("Final")
    print("\n".join(reactor.get_statuses()))
