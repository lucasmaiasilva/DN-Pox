from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import pox.lib.packet.dns as pkt_dns
from pox.lib.addresses import IPAddr
from pox.lib.revent import *

class lucas(EventMixin):
  def __init__(self, install_flow = True):
    #Event.__init__()
    self._install_flow = install_flow
    core.openflow.addListeners(self)


  def _handle_ConnectionUp (self, event):
    if self._install_flow:
      msg = of.ofp_flow_mod()
      #msg.match = of.ofp_match()
      #msg.match.dl_type = pkt.ethernet.IP_TYPE
      msg.match.dn_dst = "www.uol.com.br"
      #msg.match.dn_src = "www.uol.com"
      #msg.match.in_port=1
      msg.match.dl_type=0x0800
      msg.idle_timeout = 65535
      msg.priority = 65535
      #msg.actions.append(of.ofp_action_output(port = 3))
      msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("150.164.0.135")))
      event.connection.send(msg)
      print "regra inserida", msg

      msg = of.ofp_flow_mod()
      msg.match.dn_src="www.uol.com.br"
      msg.match.dl_type=0x0800
      #msg.match.in_port=3
      msg.idle_timeout = 65535
      msg.priority = 65535
      msg.actions.append(of.ofp_action_nw_addr.set_src(IPAddr("150.164.0.135")))
      #msg.actions.append(of.ofp_action_output(port = 1))
      event.connection.send(msg)



  def _handle_PacketIn (self, event):
    print "cacete de agulha entrada de pacote"

def launch(no_flow = False):
  core.registerNew(lucas,not no_flow)
