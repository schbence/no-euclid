import pygame
from pygame.locals import *
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *

from random import uniform


def sqr():
	a = 0.5
	vss = array([
	(-a,-a,0),
	(-a,a,0),
	(a,a,0),
	(a,-a,0),
	(0,0,0)
	])

	edges = (
	(0,1),
	(1,2),
	(2,3),
	(3,0),
	(4,2)
	)

	vss = sor(vss)
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vss[vertex])
	glEnd()


def grid():
	N = 100
	a = 0.2
	vss = []
	pra = arange(-N,N+1)
	for i in pra:
		vss.append([i*a,-N*a,0])
		vss.append([i*a,N*a,0])
	for i in pra:
		vss.append([-N*a,i*a,0])
		vss.append([N*a,i*a,0])
	e = arange(0,len(vss),2)
	ess = array([e,e+1]).T
	vss = array(vss)
	vss = sor(vss)
	glBegin(GL_LINES)
	for edge in ess:
		for vertex in edge:
			glVertex3fv(vss[vertex])
	glEnd()


def sor(vss):
	xs,ys,zs = vss.T
	return array([ys,zs,xs]).T


def S2C(vec,r):
	tas,fis = vec.T
	xs = r*sin(tas)*cos(fis)
	ys = r*sin(tas)*sin(fis)
	zs = -r*cos(tas)
	vss = array([xs,ys,zs]).T
	return vss


def UP(vss,r):
	xs,ys,zs = vss.T
	zs=zs+r
	return array([xs,ys,zs]).T


def PROJ(vss,p):
	xs,ys,zs = vss.T
	rs = p*sqrt(xs**2+ys**2)/(p-zs)
	ts = arctan2(ys,xs)
	vecp = array([rs,ts]).T
	return vecp


def P2C(vecp):
	rs,ts = vecp.T
	xs = rs*cos(ts)
	ys = rs*sin(ts)
	zs = zeros(len(rs))

	return array([xs,ys,zs]).T


def coord():
	a = 1
	vss = array([
	[0,0,0],
	[a,0,0],
	[0,a,0],
	[0,0,a]
	])


	ess = [[0,1],[0,2],[0,3]]
	vss = sor(vss)
	glBegin(GL_LINES)
	for edge in ess:
		for vertex in edge:
			glVertex3fv(vss[vertex])
	glEnd()


# Float -> (List Point, List Edge)
def sphr(r):
	vec = []
	fres = 16
	fira = pi*arange(0,fres*2)/fres
	tara = arange(-1,1,.1)*pi
	ess = zeros([1,2],dtype=int)
	for i in range(0,len(fira)):
		es = []
		v = 0
		for ta in tara:
			vec.append([ta,fira[i]])
			es.append(i*len(tara)+v)
			v+=1
		#es = array(es)
		#es = array([es,roll(es,-1)]).T
		#ess = vstack((ess,es))

	for i in range(len(tara)/2+1,len(tara)-1):
		e = arange(0,fres*2)*len(tara)+i
		es = array([e,roll(e,-1)]).T
		ess = vstack((ess,es))
	vec = array(vec)
	vss = S2C(vec,r)
	ess = ess[1:]

	return vss,ess


def roty(vss,dr):
	c = cos(dr)
	s = sin(dr)
	rmat = array([[c,0,s],[0,1,0],[-s,0,c]])
	return matmul(rmat,vss.T).T


def rotz(vss,dr):
	c = cos(dr)
	s = sin(dr)
	rmat = array([[c,-s,0],[s,c,0],[0,0,1]])
	return matmul(rmat,vss.T).T


def drawit(vss,ess):
	r = 100.
	d = r
	vss = UP(vss,d)
	vec = PROJ(vss,r)
	vss = P2C(vec)
	vss = sor(vss)
	glBegin(GL_LINES)
	for edge in ess:
		for vertex in edge:
			glVertex3fv(vss[vertex])
	glEnd()


def main():
	global vss,ess
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display,DOUBLEBUF|OPENGL)

	gluPerspective(60, (display[0]*1./display[1]),.0,10000)
	glTranslatef(0,-5.,0) # horiz,height,depth
	#glTranslate(0,0,-3)
	glRotate(10,1,0,0)
	poss = []
	vss,ess = sphr(100.)
	camx,camz=0,0
	show_grid = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:
					show_grid = -show_grid + 1

		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			vss = roty(vss,-0.01)
		if keys[pygame.K_DOWN]:
			vss = roty(vss,+0.01)
		if keys[pygame.K_LEFT]:
			vss = rotz(vss,-0.02)
		if keys[pygame.K_RIGHT]:
			vss = rotz(vss,+0.02)

		if keys[pygame.K_s]:
			glTranslatef(0,0,-0.01)
			camx-=0.01
		if keys[pygame.K_w]:
			glTranslatef(0,0,0.01)
			camx+=0.01

		if keys[pygame.K_q]:
			glTranslatef(0,-0.01,0)
			camz-=0.01
		if keys[pygame.K_a]:
			glTranslatef(0,0.01,0)
			camz+=0.01

		if keys[pygame.K_e]:
			glRotatef(1,1,0,0)
		if keys[pygame.K_d]:
			glRotatef(-1,1,0,0)

		if keys[pygame.K_p]:
			print 'CamX: ',camx,' Camz: ',camz

		#glRotate(-0.3,0,0,0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		drawit(vss,ess)

		#sqr()
		#coord()

		if show_grid:
			grid()
		pygame.display.flip()
		pygame.time.wait(10)


if __name__ == '__main__':
	main()






# ========= Le Squarre' ==========
