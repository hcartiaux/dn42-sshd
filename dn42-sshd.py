import os
import sys
import argparse

if __name__ == '__main__':

    top_directory = os.path.dirname(os.path.realpath(__file__))
    host_key_file =  top_directory + '/' + '/files/ssh-keys/ssh_host_rsa_key'

    parser = argparse.ArgumentParser(prog='dn42-sshd')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gaming', help='Start the gaming server', action='store_true')
    group.add_argument('--peering', help='Start the auto peering server', action='store_true')
    try:
        args = parser.parse_args()
    except:
        sys.exit(1)

    if args.peering:
        from src.shell_dn42 import ShellDn42
        from src.ssh_server_shell import SSHServerShell
        from src.ssh_server_auth_dn42 import SSHServerAuthDn42

        os.environ['SSH_PORT']                = os.getenv('SSH_PORT', '8022')
        os.environ['SSH_MOTD_PATH']           = os.getenv('SSH_MOTD_PATH', top_directory + '/' + 'files/motd/motd_peering_service')
        os.environ['DN42_REGISTRY_DIRECTORY'] = os.getenv('DN42_REGISTRY_DIRECTORY', top_directory + '/' + 'files/registry')
        os.environ['ASN']                     = os.getenv('ASN', '4242420263')
        os.environ['SERVER']                  = os.getenv('SERVER', 'nl-ams2.flap42.eu')
        server = SSHServerShell(ShellDn42, host_key_file)
        server.set_server_interface(SSHServerAuthDn42())

    if args.gaming:
        from src.ssh_server_pipe import SSHServerPipe
        from src.ssh_server_auth_none import SSHServerAuthNone

        os.environ['SSH_PORT']      = os.getenv('SSH_PORT', '8022')
        os.environ['SSH_MOTD_PATH'] = os.getenv('SSH_MOTD_PATH', top_directory + '/' + 'files/motd/motd_gaming_service')
        cmd = 'advent'
        server = SSHServerPipe(cmd, host_key_file)
        server.set_server_interface(SSHServerAuthNone())

    # Start the server, you can give it a custom IP address and port, or
    # leave it empty to run on 127.0.0.1:22
    server.start("::1", int(os.getenv("SSH_PORT", 8022)))
