function(ctx) {
    user_id: ctx.identity.id,
    traits: {
    email: ctx.identity.traits.email,
    name: ctx.identity.traits.name,
  }
}
