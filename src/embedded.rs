use rust_embed::RustEmbed;

#[derive(RustEmbed)]
#[folder = "src/shell/"]
struct Asset;


fn get_internal_shell_script(fname: &str) -> String {
    let asset = Asset::get(fname).unwrap();
    String::from(std::str::from_utf8(asset.data.as_ref()).unwrap())
}

pub fn get_bash_goto_enable_script_str() -> String {
    get_internal_shell_script("goto-bash.sh")
}

pub fn get_zsh_goto_enable_script_str() -> String {
    get_internal_shell_script("goto-zsh.sh")
}

pub fn get_selector_script_str() -> String {
    get_internal_shell_script("goto")
}

pub fn get_powershell_enable_script_str() -> String {
    get_internal_shell_script("goto-powershell.ps1")    
}
