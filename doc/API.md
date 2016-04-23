# API

## Python 

```py
class MyActor(Actor):
    # define any other methods or
    pass

actor = MyActor()
# or
actor = MyActor(name='foo')
```

## actor.send(msg)

msg: Dictionary.

        {'Subject': {...data}}

## actor.ask(msg [, to=target_actor_id_or_name])

Works like `actor.send`, but this is blocker.


