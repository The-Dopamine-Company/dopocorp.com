# Demo Thread Continuity Log Fields (Minimal)

Purpose: when the mocked transport prints/logs a message event, include only the fields that demonstrate **thread continuity** across inbound → agent reply → subsequent replies. These should be stable across messages in the same thread and traceable back to the original inbound email.

## Required fields to log per message

1. **thread_id**
   - Internal thread identifier used by the demo loop.
   - Must remain identical across all messages in the same conversation.

2. **message_id**
   - Unique ID for this specific message.
   - Useful for showing that each reply is a distinct message in the same thread.

3. **in_reply_to**
   - The `message_id` of the immediate parent message.
   - Shows direct linkage to the prior message in the thread.

4. **references**
   - Ordered list of all ancestor `message_id` values in the thread.
   - Demonstrates full thread lineage (can be printed as a single joined string).

5. **subject** (optional but recommended)
   - Keep unchanged or with standard `Re:` prefix.
   - Helps humans visually confirm continuity without being the source of truth.

## Suggested log format (one line)

```
[transport] thread=<thread_id> msg=<message_id> in-reply-to=<in_reply_to> refs=<references> subject="<subject>"
```

## Notes

- If `in_reply_to` is empty (new inbound message), `references` should be empty and a new `thread_id` should be created.
- For replies, `in_reply_to` must point to the most recent message in the thread; `references` should include all prior `message_id` values (including the parent).
