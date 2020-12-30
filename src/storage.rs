use dirs::config_dir;
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::Write;
use toml::value::Map;
use toml::Value;

#[derive(Serialize, Deserialize)]
pub struct Config {
    pub current_profile: String,
    pub profiles: Vec<String>,
}

fn parse_config_toml(config_name: &str) -> String {
    let mut cfg = config_dir().unwrap();
    cfg.push("goto-cd");
    cfg.push(format!("{}.toml", config_name));
    return fs::read_to_string(cfg).unwrap();
}

pub fn parse_config() -> Config {
    return toml::from_str(&parse_config_toml("_setting")).unwrap();
}

pub fn parse_profile(profile_name: &str) -> Map<String, Value> {
    let profile = parse_config_toml(profile_name);
    return toml::from_str(&profile).unwrap();
}

pub fn get_current_profile() -> Map<String, Value> {
    let setting = parse_config();
    return parse_profile(&setting.current_profile);
}


pub fn ensure_directory_structure() {
    let mut cfg1 = config_dir().unwrap();
    cfg1.push("goto-cd");
    if !cfg1.exists() {
        println!("{} does not exist! Creating!", cfg1.display());
        fs::create_dir_all(cfg1).unwrap();
    }

    let mut cfg2 = config_dir().unwrap();
    cfg2.push("goto-cd");
    cfg2.push("_setting.toml");
    if !cfg2.exists() {
        println!("{} does not exist! Writing default", cfg2.display());
        let default_config = Config {
            current_profile: String::from("default"),
            profiles: vec![String::from("default")],
        };
        let config_str = toml::to_string(&default_config).unwrap();
        let mut file = fs::File::create(cfg2).unwrap();
        write!(file, "{}", config_str).unwrap();

        let mut profile = config_dir().unwrap();
        profile.push("goto-cd");
        profile.push("default.toml");
        println!("{} does not exist! Writing default", profile.display());
        fs::File::create(profile).unwrap();
    }
}
