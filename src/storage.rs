use crate::embedded;
use crate::paths;

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
    let cfg = paths::get_config_toml_path(config_name);
    fs::read_to_string(cfg).unwrap()
}

fn write_to_current_profile(profile_name: &str, profile: &Map<String, Value>) {
    let serialized = toml::to_string(profile).unwrap();
    let cfg = paths::get_config_toml_path(profile_name);

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
        None => return false,
    }
}

pub fn ensure_directory_structure() {
    let cfg1 = paths::get_config_dir();
    if !cfg1.exists() {
        fs::create_dir_all(cfg1).unwrap();
    }

    let cfg2 = paths::get_config_toml_path("_setting");
    if !cfg2.exists() {
        let default_config = Config {
            current_profile: String::from("default"),
            profiles: vec![String::from("default")],
        };
        let config_str = toml::to_string(&default_config).unwrap();
        let mut file = fs::File::create(cfg2).unwrap();
        write!(file, "{}", config_str).unwrap();

        let profile = paths::get_config_toml_path("default");
        fs::File::create(profile).unwrap();
    }
}

fn install_local_shell(fname: &str, content: String) {
    let executable = paths::get_config_script_path(fname);
    let mut file = fs::File::create(executable).unwrap();
    write!(file, "{}", &content).unwrap();
}

pub fn install_latest_scripts() {
    let shell_dir = paths::get_config_shell_dir();
    if !shell_dir.exists() {
        fs::create_dir_all(shell_dir).unwrap();
    }

    install_local_shell("goto", embedded::get_selector_script_str());
    install_local_shell("goto-zsh.sh", embedded::get_zsh_goto_enable_script_str());
    install_local_shell("goto-bash.sh", embedded::get_bash_goto_enable_script_str());
    install_local_shell("goto-powershell.ps1", embedded::get_powershell_enable_script_str());
}
