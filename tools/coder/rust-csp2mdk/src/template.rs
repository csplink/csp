use rust_embed::RustEmbed;

#[derive(RustEmbed)]
#[folder = "template/"]
pub struct Asset;