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

fn write_to_current_profile(profile_name: &str, profile: &Map<String, Value>) {
    let serialized = toml::to_string(profile).unwrap();
    let mut cfg = config_dir().unwrap();

    cfg.push("goto-cd");
    cfg.push(format!("{}.toml", profile_name));

    let mut file = fs::File::create(cfg).unwrap();
    file.write_all(serialized.as_bytes()).unwrap();
}

fn parse_config() -> Result<Config, toml::de::Error> {
    return toml::from_str(&parse_config_toml("_setting"));
}

fn parse_profile(profile_name: &str) -> Result<Map<String, Value>, toml::de::Error> {
    let profile = parse_config_toml(profile_name);
    return toml::from_str(&profile);
}

fn get_current_profile_name() -> Result<String, toml::de::Error> {
    return Ok(parse_config()?.current_profile);
}

pub fn get_current_profile() -> Result<Map<String, Value>, toml::de::Error> {
    let current_profile = get_current_profile_name()?;
    return parse_profile(&current_profile);
}

pub fn save_to_current_profile(teleport: &str, path: &str) {
    let profile_name = get_current_profile_name().unwrap();
    let mut profile = parse_profile(&profile_name).unwrap();
    profile.insert(String::from(teleport), toml::Value::from(path));
    write_to_current_profile(&profile_name, &profile);
}

pub fn remove_from_profile(teleport: &str) -> bool {
    let profile_name = get_current_profile_name().unwrap();
    let mut profile = parse_profile(&profile_name).unwrap();

    let res = profile.remove(teleport);
    write_to_current_profile(&profile_name, &profile);
    match res {
        Some(_x) => return true,
        None => return false
    }
}

pub fn ensure_directory_structure() {
    let mut cfg1 = config_dir().unwrap();
    cfg1.push("goto-cd");
    if !cfg1.exists() {
        fs::create_dir_all(cfg1).unwrap();
    }

    let mut cfg2 = config_dir().unwrap();
    cfg2.push("goto-cd");
    cfg2.push("_setting.toml");
    if !cfg2.exists() {
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
        fs::File::create(profile).unwrap();
    }
}
