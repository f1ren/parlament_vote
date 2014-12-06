from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json
import gspread

CANDIDATES_RANGE = 'A2:A1000'
JOBS_RANGE = 'B1:T1'

@require_http_methods(["GET", "POST"])
@csrf_exempt
def post(request):
	vote = json.loads(request.body)
	vote.pop('method')
	vote.pop('url')
	all_vote_candidates = set()
	for job, candidates in vote.iteritems():
		for candidate in candidates:
			all_vote_candidates.add(candidate['name'])

	if '' in all_vote_candidates:
		all_vote_candidates.remove('')

	wks = get_worksheet()
	current_candidates = get_current_candidates(wks)

	for candidate in all_vote_candidates:
		if candidate not in current_candidates:
			current_candidates.append(candidate)
			print len(current_candidates)
			wks.update_cell(len(current_candidates) + 1, 1, candidate)

	current_jobs = [u'\u05e9\u05e8 \u05d4\u05d1\u05e8\u05d9\u05d0\u05d5\u05ea', u'\u05e9\u05e8 \u05d4\u05db\u05dc\u05db\u05dc\u05d4', u'\u05e9\u05e8 \u05d4\u05ea\u05e7\u05e9\u05d5\u05e8\u05ea', u'\u05e9\u05e8 \u05d4\u05d7\u05d5\u05e5', u'\u05e9\u05e8 \u05d4\u05d1\u05d9\u05d8\u05d7\u05d5\u05df', u'\u05e9\u05e8 \u05d4\u05ea\u05d7\u05d1\u05d5\u05e8\u05d4', u'\u05e9\u05e8 \u05d4\u05ea\u05e8\u05d1\u05d5\u05ea \u05d5\u05d4\u05e1\u05e4\u05d5\u05e8\u05d8', u'\u05e9\u05e8 \u05d4\u05d1\u05d9\u05e0\u05d5\u05d9 \u05d5\u05d4\u05e9\u05d9\u05db\u05d5\u05df', u'\u05e9\u05e8 \u05d4\u05de\u05d3\u05e2', u'\u05e9\u05e8 \u05d4\u05d7\u05d9\u05e0\u05d5\u05da', u'\u05e9\u05e8 \u05d4\u05d0\u05d5\u05e6\u05e8', u'\u05e9\u05e8 \u05d4\u05ea\u05d9\u05d9\u05e8\u05d5\u05ea', u'\u05e9\u05e8 \u05dc\u05d1\u05d9\u05d8\u05d7\u05d5\u05df \u05e4\u05e0\u05d9\u05dd', u'\u05e9\u05e8 \u05d4\u05d2\u05e0\u05ea \u05d4\u05e1\u05d1\u05d9\u05d1\u05d4', u'\u05e9\u05e8 \u05d4\u05de\u05e9\u05e4\u05d8\u05d9\u05dd', u'\u05e8\u05d0\u05e9 \u05d4\u05de\u05de\u05e9\u05dc\u05d4', u'\u05de\u05d1\u05e7\u05e8 \u05d4\u05de\u05d3\u05d9\u05e0\u05d4', u'\u05e9\u05e8 \u05d4\u05e4\u05e0\u05d9\u05dd', u'\u05e9\u05e8 \u05d4\u05d7\u05e7\u05dc\u05d0\u05d5\u05ea']
	
	for job, candidates in vote.iteritems():
		col = current_jobs.index(job) + 2
		for candidate in candidates:
			if candidate['name'] == '':
				continue
			row = current_candidates.index(candidate['name']) + 2
			val = wks.cell(row, col).value
			if val == '':
				val = 0
			else:
				val = int(val)
			wks.update_cell(row, col, val + 1)

	return HttpResponse("OK")

def get_candidates(request):
	wks = get_worksheet()
	return HttpResponse(json.dumps(get_current_candidates(wks)))

def get_current_candidates(wks):
	candidates = [c.value for c in wks.range(CANDIDATES_RANGE)]
	candidates = [c for c in candidates if c != '']
	return candidates

def get_current_jobs(wks):
	jobs = [c.value for c in wks.range(JOBS_RANGE)]
	jobs = [c for c in jobs if c != '']
	return jobs

def default_view(request, args):
	return redirect('/static/vote/vote.html')

def get_worksheet():
	gc = gspread.login('parlament.voter', '*&^%!@#$')
	return gc.open_by_url('https://docs.google.com/spreadsheets/d/1qusezQhlHj3zvGe-eg9D91pUSq5GpZ46wUNp6g1QSwY/edit#gid=0').sheet1

def spreadsheet_old():
	import gdata.spreadsheet.service
	c = gdata.spreadsheet.service.SpreadsheetsService()
	c.email="navatm@gmail.com"
	c.password = 'timP2Gml'
	c.ProgrammaticLogin()
	c.email="parlament.voter@gmail.com"
	c.password = '*&^%!@#$'
	c.ProgrammaticLogin()