function(ctx) {
    user_id: ctx.identity.id,
    email: ctx.identity.traits.email,
}
