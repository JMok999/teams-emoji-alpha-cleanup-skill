# ChatGPT Teams Emoji Quick Prompt

Use this file with an original image in a chat model. It is the default fast path for normal users.

Copy the text below after uploading the image. Do not upload the full `SKILL.md` unless you need to diagnose a failed result or explain the technical workflow.

```text
Process the uploaded image into a Teams emoji.

Do not explain this request or summarize any workflow. Preserve the original subject and do not redraw or restyle it.

Remove only the exterior background. Return one downloadable 256 × 256 transparent WEBP with clean edges and safe padding.

If you cannot produce a downloadable file from this source, reply with one short sentence only.

When complete, reply with the file link and no more than two short lines.
```

## Accept the result only when

- a downloadable file is returned
- the file is `.webp`
- it can be uploaded to Teams without a visible box, halo, or fringe
- the subject is faithful to the selected source image

For detailed requirements, troubleshooting, or local processing, use [`../SKILL.md`](../SKILL.md).
