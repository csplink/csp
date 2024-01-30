// Copyright (c) HalfSweet 2024
// All rights reserved. Licensed under GPL-v3.

use rust_embed::RustEmbed;

#[derive(RustEmbed)]
#[folder = "template/"]
pub struct Asset;