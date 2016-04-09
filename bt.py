#!/usr/bin/python
import libtorrent as lt
import time,sys,socket,GeoIP,ConfigParser
import MySQLdb as mdb
def getinfo(ip):
	gi = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)	
	gir = gi.record_by_addr(ip)
	if gir is not None:
		 return (gir['country_code'])
		
def lookupIp(addr):
	try:
		return socket.gethostbyaddr(addr)[0]
	except socket.herror:
		return "Unknown host"

def insert2db(con,seeder_ip,seeder_hostname,torrent,country_code,hash_code):
	
	with con:    
		cur = con.cursor()
		cur.execute("INSERT INTO seeder  (seeder_ip,seeder_hostname,torrent,country_code,hash) SELECT * FROM (SELECT %s,%s,%s,%s,%s) AS tmp WHERE NOT EXISTS (SELECT seeder_ip,seeder_hostname,torrent,country_code,hash FROM seeder WHERE seeder_ip = %s AND seeder_hostname=%s AND torrent=%s AND country_code=%s AND hash=%s ) LIMIT 1;",(seeder_ip,seeder_hostname,torrent,country_code,hash_code,seeder_ip,seeder_hostname,torrent,country_code,hash_code))
		
#MAIN
def main():
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'bit-tracker.config'))
	ses = lt.session()
	ses.listen_on(6881, 6891)
	info = lt.torrent_info(config.get('Torrents', 'torrent_file'))
	h = ses.add_torrent({'ti': info, 'save_path': config.get('Torrents', 'torrent_save_path')})
	con = mdb.connect(config.get('Settings', 'database_host'), config.get('Settings', 'database_user'), config.get('Settings', 'database_password'), config.get('Settings', 'database_name'));
	while (not h.is_seed()):
		s = h.status()
		p = h.get_peer_info()	
		state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
		print '\r%.2f%% complete (bitrate: %.1f kb/s envoi: %.1f kB/s Peers: %d) %s' % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,s.num_peers, state_str[s.state]),
		for i in p:
			print "Seeder IP ",i.ip[0]," Port",i.ip[1]," hostname ",lookupIp(i.ip[0])				
			insert2db(con,i.ip[0],lookupIp(i.ip[0]), h.name(),getinfo(i.ip[0]),info.info_hash())
		sys.stdout.flush()
		time.sleep(1)
	print h.name(), 'complete'

if __name__ == "__main__":
	main()
